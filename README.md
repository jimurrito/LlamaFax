# LlamaFax
 AI generated Llama facts
 
# Current Architecture

<img src="https://drive.google.com/file/d/1qnWysIuh3Iv1Nn1-RH2xQz0q__5b0awz/view?usp=sharing" alt="Architecture Diagram">

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2022-06-24T19:52:24.760Z\&quot; agent=\&quot;5.0 (Windows)\&quot; etag=\&quot;-bstBQq-QewZ-e57sAst\&quot; version=\&quot;20.0.3\&quot; type=\&quot;google\&quot;&gt;&lt;diagram id=\&quot;XKDfDnqy39f_5Dwoot7K\&quot; name=\&quot;Service Architecture\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
