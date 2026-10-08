import json, re, sys, os
SRC = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/Bestandcheck/ktw_data.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'appdata.json'
d=json.load(open(SRC, encoding='utf-8'))
# checklist definition: section -> items
# item: (label, soll, excel-alias-list or None)  ; sections with ablauf flag
C=[
 ("Notfalltasche",True,[
  ("Hyperventilationsmaske","1",["Hyperventilationsmaske"]),
  ("Beatmungsbeutel Erwachsener","1",["Beatmungsbeutel Erwachsener"]),
  ("Beatmungsmaske Größe 3 (Adult S)","1",["Beatmungsmaske Gr. 3 (Adult S)"]),
  ("Beatmungsmaske Größe 5 (Adult L)","1",["Beatmungsmaske Gr. 5 (Adult L)"]),
  ("Güdeltubus Größe 1 (7 cm)","1",["Güdeltubus 1 (7cm)"]),
  ("Güdeltubus Größe 2 (8 cm)","1",["Güdeltubus 2 (8cm)"]),
  ("Güdeltubus Größe 3 (9 cm)","1",["Güdeltubus 3 (9cm)"]),
  ("Güdeltubus Größe 4 (10 cm)","1",["Güdeltubus 4 (10cm)"]),
  ("Güdeltubus Größe 5 (11 cm)","1",["Güdeltubus 5 (11cm)"]),
  ("Thorax-Dekompressionsnadel","1",["Thorax-Dekommpressionsnadel","Thorax-Dekompressionsnadel"]),
  ("Thorax-Verschlußpflaster","1",["Thorax-Verschlusspflaster","Thorax-Verschlußpflaster"]),
  ("Blutdruckmanschette","1",["Blutdruckmanschette"]),
  ("Set Verbandsstoff","1",["Set Verbandsstoff"]),
  ("Kopfverband","1",["Kopfverband"]),
  ("sterile Handschuhe","2",["sterile Handschuhe"]),
  ("Wunddesinfektion Sprühflasche","1",["Wunddesifektion Sprühflasche","Wunddesinfektion Sprühflasche"]),
  ("Hämostatikum (Verband)","1",["Hämostatikum (Verband)"]),
  ("Pulsoximeter","1",["Pulsoximeter"]),
  ("Tourniquet","1",["Tourniquet"]),
  ("Schiene","1",["Schiene"]),
  ("Kaltkompresse","1",["Kaltkompresse"]),
  ("Kanülensammelbox","1",["Kanülensammelbox"]),
  ("Stethoskop","1",["Stethoskop"]),
  ("Kohlenmonoxid-Warner","1",["Kohlenmonoxid-Warner"]),
 ]),
 ("Notfalltasche und Fächer im Patientenraum",True,[
  ("Sauerstoffmasken","je 2",["Sauerstoffmasken"]),
  ("Sauerstoffbrillen","je 3",["Sauerstoffbrillen"]),
  ("Sauerstoffleitung","je 1",["Sauerstoffleitung"]),
  ("O2-Leitungsverbindungsstück (Fingertip)","je 1",["O2-Leitungsverbindungsstück (Fingertip)"]),
 ]),
 ("Fächer im Patientenraum",True,[
  ("Hautdesi: Sterillium classic pure (blau)","2",["Hautdesi: Sterillium classic pure (blau)"]),
  ("Hautdesi: Sterillium Virugard (weiß)","1",["Hautdesi: Sterillium Virugard (weiß)"]),
  ("Entbindungs-/Notgeburt-Set","1",["Entbindungs-/Notgeburt-Set"]),
  ("Hautschutzcreme Baktolan","1",["Hautsschutzcreme Baltolan","Hautschutzcreme Baktolan"]),
  ("Desinfektionstücher (Microbac Tissues)","2 Pck.",["Desinfektionstücher Microbac Tissues"]),
  ("FFP2 Masken","10",["FFP2"]),
  ("FFP3 Masken","4",["FFP3"]),
  ("Steckbecken","1",["Steckbecken"]),
  ("Urinflasche","1",["Urinflasche"]),
  ("Handschuhe (unsterile)","2 Pck.",["Handschuhe (unsterile)"]),
  ("Spanngurte","2",["Spanngurte"]),
  ("Wasserflasche 0,5 (Sommer)","1",["Wasserflasche 0,5"]),
  ("Müllbeutel","1",["Müllbeutel"]),
  ("Nierenschalen","5",["Nierenschalen"]),
  ("Papiertücher","15",["Papiertücher"]),
  ("Einmaldecken","4",["Einmaldecken"]),
  ("Einmallaken (im Zipbeutel verpackt)","3",["Einmallaken"]),
  ("Schutzkittel (im Zipbeutel verpackt)","4",["Schutzkittel"]),
  ("Kontaminationsbeutel","2",[]),
  ("Schutzbrillen","2",["Schutzbrillen"]),
  ("Mundschutz (im Karton/Zipbeutel verpackt)","10",["Mundschutz"]),
  ("Brechbeutel","5",["Brechbeutel"]),
  ("Stifneck","1",["Stifneck"]),
 ]),
 ("Geräte und deren Zubehör",False,[
  ("Krankentrage","",{"dev":[("sn","S-Nr. Unterteil","text",["Krankentrage-Unterteil"],"sn"),("date","TÜV Unterteil bis","month",["Krankentrage-Unterteil"],"mhd"),("sn","S-Nr. Oberteil","text",["Krankentrage-Oberteil"],"sn"),("date","TÜV Oberteil bis","month",["Krankentrage-Oberteil"],"mhd")]}),
  ("Ambulanzdecke","1",["Ambulanzdecke"]),
  ("Tragetuch","1",["Tragetuch"]),
  ("Rollboard","1",["Rollboard"]),
  ("Krankentragestuhl","",{"dev":[("sn","S-Nr.","text",["Krankentragestuhl"],"sn"),("date","TÜV bis","month",["Krankentragestuhl"],"mhd")]}),
  ("Defibrillator","",{"dev":[("sn","S-Nr.","text",["Defibrillator"],"sn"),("date","TÜV/STK bis","month",["Defibrillator"],"mhd"),("date","Ablaufdatum Akku","month",["Defibrillator"],"akku"),("date","Ablaufdatum Pads","month",["Defibrillator"],"pads")]}),
  ("Einmalrasierer","2",["Einmalrasierer"]),
  ("Feuerlöscher","",{"dev":[("date","TÜV bis","month",["Feuerlöscher"],"mhd"),("sn","S-Nr.","text",["Feuerlöscher"],"sn")]}),
  ("Absaugpumpe ACCUVAC Rescue","",{"dev":[("check","Funktionstest","check",["Absaugpumpe"],None)]}),
  ("Absaugkatheter Schwarz (Ø 3,33 mm)","1",["Absaugkatheter Schwarz (3,33mm)"],True),
  ("Absaugkatheter Weiß (Ø 4 mm)","1",["AbsaugkatheterWeiß (4mm)","Absaugkatheter Weiß (4mm)"],True),
  ("Absaugkatheter Grün (Ø 4,67 mm)","1",["Absaugkatheter Grün (4,67mm)"],True),
  ("Absaugkatheter Orange (Ø 5,33 mm)","1",["Absaugkatheter Orange (5,33mm)"],True),
  ("Absaugkatheter Rot (Ø 6 mm)","1",["Absaugkatheter Rot (6mm)"],True),
  ("Sauerstoffgerät 2l","",{"dev":[("num","Füllstand in bar","number",None,None),("sn","S-Nr. Druckminderer","text",["O2-Flasche klein 2l","O2-Flasche groß 2l"],"sn"),("date","TÜV Druckminderer bis","month",["O2-Flasche klein 2l","O2-Flasche groß 2l"],"mhd")]}),
  ("Sauerstoffgerät 10l","1",{"dev":[("num","Füllstand in bar","number",None,None),("sn","S-Nr. Druckminderer","text",["O2-Flasche groß 10l"],"sn"),("date","TÜV Druckminderer bis","month",["O2-Flasche groß 10l"],"mhd")]}),
 ]),
 ("Fahrerkabine",False,[
  ("Warndreieck","2",["Warndreieck"]),("Warnwesten","2",["Warnwesten"]),("Abschlepphaken","1",["Abschlepphaken"]),
  ("Sicherheits-/Schutzhandschuhe","1 Paar",["Sicherheitshandschuhe"]),("Feuerwehrdreikant","1",["Feuerwehrdreikant"]),
  ("Warnleuchte","1",["Warnleuchte"]),("Notfallhammer inkl. Gurtmesser","1",["Notfallhammer /inkl. Gurtmesser"]),
  ("Handbesen","1",["Handbesen"]),("Ersatzbatterien AA/AAA","je 4",[]),
 ]),
 ("Fahrzeugmappe",False,[
  ("Fahrzeugschein","1",["Fahrzeugschein (TÜV)","Fahrzeugschein"]),("Tankkarte","1",["Tankkarte"]),
  ("Verletztenanhängekarten","1",[]),("Auszug Genehmigungsurkunde","1",["Auszug Genehmigungsurkunde"]),
  ("Desinfektionsbuch","1",["Desinfektionsbuch"]),("Transportscheine","20",["Transportscheine"]),
  ("Muster Transportvertrag","10",["Transportvertrag"]),("Datenschutzblätter","3",["Datenschutzblätter"]),
  ("AGB-Blätter","3",["AGB-Blätter"]),("Hygieneplan","1",["Hygieneplan"]),("Quittungsblock","1",["Quittungsblock"]),
 ]),
]
norm=lambda s: re.sub(r"\s+"," ",(s or "")).strip().lower()
# build checklist definition (vehicle independent) + per vehicle values
secs=[]; used_names=set()
for title,abl,items in C:
    out=[]
    for it in items:
        label,soll,spec=it[0],it[1],it[2]
        ablauf = abl or (len(it)>3 and it[3])
        if isinstance(spec,dict):
            out.append({"t":label,"s":soll,"dev":[{"k":f[0],"l":f[1],"ty":f[2],"xl":f[3],"col":f[4]} for f in spec["dev"]]})
            for f in spec["dev"]:
                for n in (f[3] or []): used_names.add(norm(n))
        else:
            out.append({"t":label,"s":soll,"a":bool(ablauf),"xl":spec})
            for n in spec: used_names.add(norm(n))
    secs.append({"t":title,"a":abl,"items":out})
ORT = {"notfalltasche":0, "notfalltasche/fächer pat.-raum":1, "fächer im pat.-raum":2,
       "geräte und deren zubehör":3, "fahrerkabine":4, "fahrzeugmappe":5}
veh=[]; unmatched={}
for v in d:
    byname={}
    for x in v['items']:
        byname.setdefault(norm(x['name']),{"r":x['row'],"sn":x['sn'],"mhd":x['mhd'],"pads":x['pads'],"akku":x.get('akku',''),"name":x['name'],"ort":x.get('ort') or ""})
    vals={}; hide=[]; miss=[]
    for si,s in enumerate(secs):
        for ii,it in enumerate(s["items"]):
            if "dev" in it:
                linked=[f for f in it["dev"] if f["xl"]]; found=0
                for fi,f in enumerate(it["dev"]):
                    if not f["xl"]: continue
                    hit=next((byname[norm(n)] for n in f["xl"] if norm(n) in byname),None)
                    if not hit: miss.append(it["t"]+"/"+f["l"]); continue
                    found+=1
                    vals[f"{si}.{ii}.{fi}"]={"r":hit["r"],"n":hit["name"],"col":f["col"],"v":hit[f["col"]] if f["col"] else ""}
                if linked and not found: hide.append(f"{si}.{ii}")      # Gerät steht nicht mehr in der Excel
            elif it["xl"]:
                hit=next((byname[norm(n)] for n in it["xl"] if norm(n) in byname),None)
                if not hit: miss.append(it["t"]); hide.append(f"{si}.{ii}"); continue   # Material aus der Excel entfernt/umbenannt
                vals[f"{si}.{ii}"]={"r":hit["r"],"n":hit["name"],"col":"mhd","v":hit["mhd"]}
    # Materialien, die nur in der Excel stehen (neu hinzugefügt oder umbenannt) -> im passenden Bereich anhängen
    extra=[{"t":b["name"],"n":b["name"],"r":b["r"],"mhd":b["mhd"],"sec":ORT.get(norm(b["ort"]),"x")}
           for k,b in byname.items() if k not in used_names]
    unmatched[v["id"]]=(miss,[e["t"] for e in extra])
    veh.append({"id":v["id"],"kz":v["kz"],"vals":vals,"hide":hide,"extra":extra})
for k,(m,e) in unmatched.items():
    if m or e: print(k,"ausgeblendet:",m,"| zusätzlich aus Excel:",e)
json.dump({"secs":secs,"veh":veh},open(OUT,"w",encoding="utf-8"),ensure_ascii=False,separators=(',',':'))
print("App-Daten:", OUT, os.path.getsize(OUT), "Bytes")
