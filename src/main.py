#!/bin/python3
from functions.rsa_encrypt import rsa_encrypt
from functions.rsa_decrypt import rsa_decrypt

cipher_int = 378849509714148947484152449975953821556861364458971341826368676434335839252992929746831147224257682576639011713711856096605547503921605801439520528324485797404163487930990155803066904216312266694274127450513029433391421149265014122702791778116572169280794918054106178414105714822668278748432840859426816157747873857248445363719406752335247854850256431258832724974141280384444576950580599083379800445185638591658036068697204956531875909564286071826038606222666088063117590295883665200948768461962829724723658092901866913607412510601363966684768810162124683642376314328521677895468574221130528781227242032180584046506409485365959883750481405170829096572883630148478794052969209492175093606394969751452779261378347333674241530969559708677742928786491667772194519050686116785151595366098566341267522860740876843250610857857050175278020310949198303768612013145902863612825977875025951282095409195403243981716162280205752442750123726496711389423786246555658564451804405558898820002451339147393710586865278343545581501108859637845029442095283691514380481919323535222756884386099410483201147938288332073827465618224902868656348047440147766824174761592253209384731298362292701261373819291055127411579253563197957046905847134460447524470225952

n_correcta = 670072836834044047175556786113952556351093389215234290414019206080089839692602404219654804214111225791735425527682618411820147789768050074011237586702689389862714205745436484131812672393798547664191001956262397346816264300253017131421588546443612905935907921787472366620506826067876335209992866607147144739261646945219769079331750868720511462034491330435931264140788969834397932552237652082045479756351358662855991369505115749394497233363096456521519197523548536995784772099920753494135709818326473243605390036233043167526339197833041940424596750400286380295463571322339472759685673789937024176300917070525788585194995426221654293579495652463093593791295397626273693798789949487250836582928249757179404894849743546604167003110471807389814198157459912252695757122950137429749085897621217645414309192917293718164792777932190944773986568486281038575012673030486749322306877603792679238912375654506707964791846883426618340423164400987232235774392202322875038328114927315976326845700207644963701065320881158800849019632423478813371288031672722943884047022472972109137521815935345757551396491416425747655483705009735819840469199845041309896006800543630087739570198512655394955287799282038334474354581872653639102529241261304074190872826681

n_otra = 616324242688715408618362253814211270705153742735486265593505457024800351318437101585499708982274020356959601757583564416073286946422325181987746096914010314620514276618760314898895044951892597383633297118917353774668891112702328571722205883313537193172195062215925029021431292169550866897185195423581070810581816839650445036520477507544539487068845566541248958175460050489392740970884361758601757833698526888709720644155325537953065666405093463903595309321146499238206527103395947714638191704191558876247651697028628379393887270028829165886405506005458482212858779423007505629763973439163664894846082807164304771374136252990156776079825282374797593820985981326017823495828919405835797176825731692568553752386892432039777321360443324703972040591912946754422261912783722700138434594179495186413754065695528924650532611800492406520418322303112962051532529365913500877733054379355507825653025987739740432511226675457054923736277001455333618927380320865738396301550076901076091103469352591023977213019025396351631258302844771900637257289332563292428213846813192695372700608817924462513067293998037197564104636805432052197257376764516321862334849465433158120447282276296061727238789240475444056829842604626003382942028834546657630086260903

d_correcta = 379312940380337826054991549934258905474300221958526892290915033131898819945311146285990716412702936747907175361269167957949183863353600099115658379679922390016583522574270230935290268598463956540485862666514773016304325637046045479021156193974573068607294322144642527568460300903186660359118137208882797849792755848157654654227819788495998515800503438787900178042313959929296868940529237752594797648364726109423599246490841649553480520324969337023236350594719428323033084519202283196956539032151209711529614797049142750996531087788699863402537724386227999795251583570921343667112910446509203349506198367325880506006487896647531634800788552310070083762495034670871485018895241993015942916875369138112132554546600332366029418219921817816943728283422713820589829179602322068764407054425674016051481396798536175672654086712874246775687499090430759781826827021971034437347687774044761366732191856014215161432041069526447770982351674794806767365684013956120654535172647388430144724699472976612656725238583398361610050441041741345480720092522265874898617598970506711571293118929865094700486438263240494335411486651331449623675096598196440618829107316451550180924912859072718028697632177826537584313649446217697588361693455722627683414188301

d_otra = 566180951692541788239750057080497879866392741220836330928437310834766698981132882203259379881254976510837432653544081902889852153887973016487972500491447441776829302895043483200146118701324348466997919542310744831224202960773970301669826284463608445838717117364386016635416191541691104895632004676391936892916646822881044958171953985408532581884734536729113226527817451816743060716115980281011014089412390120615358215685359018759850442435855348800158011469545828869741122789568534296043339358695893955238870720655638365830126235440829759253414765537919464144302650642570866479087233484975638875661205355834520480958494373361652259245364394442068099835891291442347005378590210372235259594816118912956766187767642892125366990826158158679843479099949123037240518157526632701339358234940561067329276504095808576214723776368929706503987170815941605490503082105009280819717305858666803561581808886680899631696661451351346461885748332277815421124644507180113031916380653158439027615505741264183366584781076766214817431541186743137059914042655266941698705030262612887773477218621810831263428066855426429608105108335820069009101091985658622694937860120193831647102379744617992736059817373066814993782597215315470276149734498947596161163462473

test = 198709817091870918701987

rsa_decrypt(cipher_int, n_correcta, test)
