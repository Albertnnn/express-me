<map version="0.8.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1286297354401" ID="Freemind_Link_1086084505" MODIFIED="1286297429920" TEXT="ExpressMe">
<font NAME="Verdana" SIZE="12"/>
<node CREATED="1286349623008" ID="Freemind_Link_956306935" MODIFIED="1286349634727" POSITION="right" TEXT="entry.py: application entry point"/>
<node CREATED="1286323599177" ID="Freemind_Link_305211673" MODIFIED="1286323603883" POSITION="right" TEXT="framework">
<node CREATED="1286323609129" ID="Freemind_Link_97759747" MODIFIED="1286346220698" TEXT="web: web mvc that app uses">
<icon BUILTIN="button_ok"/>
</node>
<node CREATED="1286323800823" ID="Freemind_Link_94254994" MODIFIED="1286346223183" TEXT="view: templating system using Cheetah and also part of mvc, but not touched by app">
<icon BUILTIN="button_ok"/>
</node>
<node CREATED="1286324480793" ID="Freemind_Link_1861162948" MODIFIED="1286324488396" TEXT="validator: validate data"/>
<node CREATED="1286323646321" ID="Freemind_Link_250667981" MODIFIED="1286323665019" TEXT="encode: encode html/xml/json/etc"/>
<node CREATED="1286323671801" ID="Freemind_Link_1820657933" MODIFIED="1286346228698" TEXT="cache: memcache api &amp; impl">
<icon BUILTIN="button_ok"/>
</node>
<node CREATED="1286323689425" ID="Freemind_Link_628384034" MODIFIED="1286323702531" TEXT="store: backend storage api &amp; impl">
<node CREATED="1286323720361" ID="Freemind_Link_144838318" MODIFIED="1286323734291" TEXT="User: store users of system"/>
<node CREATED="1286323737457" ID="Freemind_Link_877655052" MODIFIED="1286323768547" TEXT="ShardedCounter: store counters that can be used for any data"/>
<node CREATED="1286323771850" ID="Freemind_Link_929387311" MODIFIED="1286323785059" TEXT="Comment: store comments for any data"/>
</node>
<node CREATED="1286324499073" ID="Freemind_Link_889870484" MODIFIED="1286324526155" TEXT="recaptcha: captcha api &amp; impl using google reCaptcha service"/>
<node CREATED="1286324459114" ID="Freemind_Link_640671742" MODIFIED="1286324472987" TEXT="mail: send mail asynchronized"/>
<node CREATED="1286324424209" ID="Freemind_Link_638328517" MODIFIED="1286346234086" TEXT="gaeunit: base testcase for testing with gae-infrastructure">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node CREATED="1286323265019" ID="_" MODIFIED="1286323269496" POSITION="right" TEXT="manage">
<node CREATED="1286323273555" ID="Freemind_Link_1565758848" MODIFIED="1286323276830" TEXT="urls">
<node CREATED="1286323575618" ID="Freemind_Link_1470216928" MODIFIED="1286346240444" TEXT="/">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323583569" ID="Freemind_Link_1742079265" MODIFIED="1286323593864" TEXT="GET/POST: do management task"/>
</node>
<node CREATED="1286323279850" ID="Freemind_Link_1252708827" MODIFIED="1286325315181" TEXT="/signin">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323385655" ID="Freemind_Link_1783794629" MODIFIED="1286323390980" TEXT="GET: show signin page"/>
<node CREATED="1286323393727" ID="Freemind_Link_334555583" MODIFIED="1286323401087" TEXT="POST: do signin"/>
</node>
<node CREATED="1286323356626" ID="Freemind_Link_1272818183" MODIFIED="1286325317822" TEXT="/g_signin">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323443696" ID="Freemind_Link_1995606365" MODIFIED="1286323456860" TEXT="GET: handle Google signin callback"/>
</node>
<node CREATED="1286323293753" ID="Freemind_Link_1033924223" MODIFIED="1286325325552" TEXT="/register">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323404728" ID="Freemind_Link_134139364" MODIFIED="1286323409947" TEXT="GET: show register page"/>
<node CREATED="1286323412242" ID="Freemind_Link_1228730025" MODIFIED="1286323418404" TEXT="POST: do register"/>
</node>
<node CREATED="1286323338439" ID="Freemind_Link_1131187183" MODIFIED="1286325329566" TEXT="/forgot">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323494481" ID="Freemind_Link_110313623" MODIFIED="1286323501363" TEXT="GET: show forgot password page"/>
<node CREATED="1286323506002" ID="Freemind_Link_525092194" MODIFIED="1286323516883" TEXT="POST: handle forgot password form submit"/>
</node>
<node CREATED="1286323377122" ID="Freemind_Link_368358558" MODIFIED="1286325335658" TEXT="/signout">
<icon BUILTIN="button_ok"/>
<node CREATED="1286323528970" ID="Freemind_Link_1458056505" MODIFIED="1286323545906" TEXT="GET/POST: handle signout request and redirect"/>
</node>
</node>
</node>
<node CREATED="1286324542945" ID="Freemind_Link_1721396936" MODIFIED="1286324545943" POSITION="right" TEXT="apps">
<node CREATED="1286324559735" ID="Freemind_Link_891662110" MODIFIED="1286324570389" TEXT="blog">
<node CREATED="1286325014754" ID="Freemind_Link_1725613041" MODIFIED="1286325024975" TEXT="/: display all posts"/>
<node CREATED="1286324979457" ID="Freemind_Link_429958525" MODIFIED="1286324992628" TEXT="/post/$: display a single post"/>
<node CREATED="1286324995562" ID="Freemind_Link_343797958" MODIFIED="1286325012020" TEXT="/cat/$: display posts by category"/>
<node CREATED="1286325031000" ID="Freemind_Link_18149406" MODIFIED="1286325040411" TEXT="/page/$: display a single page"/>
</node>
<node CREATED="1286324571826" ID="Freemind_Link_186626770" MODIFIED="1286324575676" TEXT="wiki">
<node CREATED="1286325087375" ID="Freemind_Link_1663445223" MODIFIED="1286325100664" TEXT="/: redirect to /Main_Page"/>
<node CREATED="1286325103345" ID="Freemind_Link_1302566385" MODIFIED="1286325115560" TEXT="/$: display a wiki page"/>
<node CREATED="1286325123001" ID="Freemind_Link_98085174" MODIFIED="1286325142272" TEXT="/edit/$: edit a wiki page"/>
<node CREATED="1286325147951" ID="Freemind_Link_199480811" MODIFIED="1286325175106" TEXT="/comment/$: make a comment on a wiki page"/>
</node>
<node CREATED="1286324578370" ID="Freemind_Link_597391906" MODIFIED="1286324581147" TEXT="forum">
<node CREATED="1286325220111" ID="Freemind_Link_252702698" MODIFIED="1286325227972" TEXT="/: display all boards"/>
<node CREATED="1286325230544" ID="Freemind_Link_194047203" MODIFIED="1286325261755" TEXT="/$: display topics of a board"/>
</node>
</node>
<node CREATED="1286346283052" ID="Freemind_Link_1460885295" MODIFIED="1286346292092" POSITION="right" TEXT="theme"/>
<node CREATED="1286324593096" ID="Freemind_Link_5030493" MODIFIED="1286324597756" POSITION="right" TEXT="widgets">
<node CREATED="1286324934007" ID="Freemind_Link_18484923" MODIFIED="1286324938651" TEXT="categories"/>
<node CREATED="1286324630530" ID="Freemind_Link_920618336" MODIFIED="1286324648561" TEXT="rss subscriber"/>
<node CREATED="1286324621207" ID="Freemind_Link_53323437" MODIFIED="1286324627480" TEXT="google adsense"/>
<node CREATED="1286324870738" ID="Freemind_Link_1313259669" MODIFIED="1286324894323" TEXT="recent comments"/>
<node CREATED="1286324907826" ID="Freemind_Link_826719125" MODIFIED="1286324918683" TEXT="arbitrary text"/>
</node>
<node CREATED="1286324606186" ID="Freemind_Link_250055508" MODIFIED="1286324610754" POSITION="right" TEXT="plugins">
<node CREATED="1286324661863" ID="Freemind_Link_1981713316" MODIFIED="1286324670676" TEXT="google analytics"/>
<node CREATED="1286324678618" ID="Freemind_Link_1216297686" MODIFIED="1286325282904" TEXT="akismet anti-spam"/>
</node>
</node>
</map>
