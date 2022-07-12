from lib.General import *
from lib.ScalelibWeb import *
import streamlit as st
from datetime import datetime as DT
import logging

# Local host works, as its the relation between the service and the server, not the browser :)
DBHost = "LFXMongo" #"127.0.0.1"
RendQNam = "render"
ArchDBNam = "archive"
CorpDBNam = "corpus"
UAuthDBNam = "userAuth"
BugRepDBNam = "repBugs"

RO = False


rndQueue = Queue(RendQNam, Host=DBHost)
ArchiveDB = Database(ArchDBNam, Index="raw", Host=DBHost)
CorpusDB = Database(CorpDBNam, Host=DBHost)
UAuthDB = UAuth(UAuthDBNam, Host=DBHost)
BugRepDB = Database(BugRepDBNam, Host=DBHost)


# Auth Screen
# returns Login Screen Conatiner Object, and user Input
Popout, Upn, Pwd = STLogin()

# Missing Input Catch
if Upn or Pwd:
    if not Upn:
        st.error("Please enter a Username/Email")
    if not Pwd:
        st.error("Please enter a Password")

# all inputs submited
if Upn and Pwd:

    auth = UAuthDB.valCreds(Upn, Pwd)

    # If Auth validation fails
    if not auth:
        st.error("Username or Password is incorrect")

    # if Auth validation successeded
    else:
        logging.info(f"User Login: {auth['upn']}")
        # Removes Popout Element when successfully Autheticated
        Popout.empty()

        # Post-Signon side bar
        STsidebar(auth, UAuthDB)

        # Verbose Output user Auth Object
        logging.debug("user Auth object", auth)

        message = STMessagePeristence(rndQueue)

        Buttontxt = "Submit"

        # Main Options Page
        with st.form("Freddy the form", clear_on_submit=True):  # clear_on_submit=True
            progBar(CorpusDB)
            st.header("LlamaFax Corpus Generator")
            st.write("Input the ID of the statments that are coherent and/or funny")

            Opts = STdrawOptions(message)

            if Opts:

                logging.info(f"[{auth['upn']}] User Input Received")
                logging.debug(f"[{auth['upn']}] : {Opts}")

                Buttontxt = "Next -->"
                st.info("Please select 'Next' above")
                # Binds ratings with user input, outputs dict with statments and ratings.
                # replaces the list of unranked statments
                message["render"] = rateFaxNew(Opts, message["render"])

                logging.debug(f"[{auth['upn']}] : {message}")

                # Read-Only check
                if not RO:

                    logging.info(f"[{auth['upn']}] Pushing to MongoDB")
                    # [Pushes]
                    # Push to Archive DB
                    # Archival Data of ALL renders, and components.
                    ArchiveDB.push(message)

                    # Push to Corpus DB
                    # Data used to train NLN used to rate future renders automatically
                    CorpusDB.push(message["render"])

                    # Deletes from Render Queue
                    st.session_state["messageState"] = False
                    del Opts

                    # Adds to user score
                    UAuthDB.addtoScore(auth)
                    logging.info(f"[{auth['upn']}] User Score Increased")

            st.form_submit_button(
                Buttontxt,
            )

        # Line break between forms
        st.markdown("***")

        # Bug Submission
        with st.form("Phillip the form", clear_on_submit=True):
            st.subheader("Submit Feedback / Report a Bug")
            st.write(
                """We always looking for feedback to improve the usability of this platform. 
                \nPlease Submit any Feedback or Bugs encountered.
                """
            )
            # "Example: 'Frozen Screen', 'Score not Updating', 'Repeating Questions'  "
            BugRep = st.text_area(
                "Ensure to include as much detail as possible.", max_chars=500
            )
            st.form_submit_button("Submit")

            if BugRep:
                logging.info(f"[{auth['upn']}] User submittied Feedback/Report")
                st.info("Submitted. Thank you for your Contribution!")

                # Structure Data into Dict && Push to BugReportDB
                BugRepDB.push(
                    {
                        "BugID#": f"BgID{makeXDigits(BugRepDB.count()+1)}",
                        "SubUsr": auth["upn"],
                        "SubEml": auth["email"],
                        "Time": DT.now().isoformat(),
                        "State": "Open",
                        "Data": BugRep,
                    }
                )

                # Clear Bug-Var
                del BugRep
