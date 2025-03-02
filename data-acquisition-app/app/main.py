import os
import time
import json
from kafka import KafkaProducer
import github_requests as gr


# Initialize the producer
KAFKA_BROKER_URI = os.getenv("KAFKA_BROKER_URI", "localhost:9094")
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URI)
print("Sucessfully connected to Kafka")


# Initialize the GitHub token
def get_github_token():
  token = os.getenv("GITHUB_TOKEN", "")
  if not token:
    token_file_path = '../../keys/GIT_API_TOKEN.txt'
    try:
      with open(token_file_path, 'r') as file:
        token = file.read().strip()
    except FileNotFoundError:
      pass
  return token

GITHUB_TOKEN = get_github_token()
if GITHUB_TOKEN:
  print("GitHub token found and loaded.")
else:
  print("No GitHub token found. Slowing down requests.")
HEADERS = {'Authorization': 'token ' + GITHUB_TOKEN} if GITHUB_TOKEN else {}
# 60 requests per hour without token, 5000 with token
wait_between_requests = 0.73 if GITHUB_TOKEN else 60.05
  

# Language list (long version)
# LANGUAGES = ["A# .NET","A# (Axiom)","A-0 System","A+","A++","ABAP","ABC","ABC ALGOL","ABLE","ABSET","ABSYS","ACC","Accent","Ace DASL","ACL2","ACT-III","Action!","ActionScript","Ada","Adenine","Agda","Agilent VEE","Agora","AIMMS","Alef","ALF","ALGOL 58","ALGOL 60","ALGOL 68","ALGOL W","Alice","Alma-0","AmbientTalk","Amiga E","AMOS","AMPL","APL","App Inventor for Android's visual block language","AppleScript","Arc","ARexx","Argus","AspectJ","Assembly language","ATS","Ateji PX","AutoHotkey","Autocoder","AutoIt","AutoLISP / Visual LISP","Averest","AWK","Axum","B","Babbage","Bash","BASIC","bc","BCPL","BeanShell","Batch (Windows/Dos)","Bertrand","BETA","Bigwig","Bistro","BitC","BLISS","Blue","Bon","Boo","Boomerang","Bourne shell","bash","ksh","BREW","BPEL","C","C--","C++","C#","C/AL","Caché ObjectScript","C Shell","Caml","Candle","Cayenne","CDuce","Cecil","Cel","Cesil","Ceylon","CFEngine","CFML","Cg","Ch","Chapel","CHAIN","Charity","Charm","Chef","CHILL","CHIP-8","chomski","ChucK","CICS","Cilk","CL","Claire","Clarion","Clean","Clipper","CLIST","Clojure","CLU","CMS-2","COBOL","Cobra","CODE","CoffeeScript","Cola","ColdC","ColdFusion","COMAL","Combined Programming Language","COMIT","Common Intermediate Language","Common Lisp","COMPASS","Component Pascal","Constraint Handling Rules","Converge","Cool","Coq","Coral 66","Corn","CorVision","COWSEL","CPL","csh","CSP","Csound","CUDA","Curl","Curry","Cyclone","Cython","D","DASL","DASL","Dart","DataFlex","Datalog","DATATRIEVE","dBase","dc","DCL","Deesel","Delphi","DinkC","DIBOL","Dog","Draco","DRAKON","Dylan","DYNAMO","E","E#","Ease","Easy PL/I","Easy Programming Language","EASYTRIEVE PLUS","ECMAScript","Edinburgh IMP","EGL","Eiffel","ELAN","Elixir","Elm","Emacs Lisp","Emerald","Epigram","EPL","Erlang","es","Escapade","Escher","ESPOL","Esterel","Etoys","Euclid","Euler","Euphoria","EusLisp Robot Programming Language","CMS EXEC","EXEC 2","Executable UML","F","F#","Factor","Falcon","Fancy","Fantom","FAUST","Felix","Ferite","FFP","Fjölnir","FL","Flavors","Flex","FLOW-MATIC","FOCAL","FOCUS","FOIL","FORMAC","@Formula","Forth","Fortran","Fortress","FoxBase","FoxPro","FP","FPr","Franz Lisp","Frege","F-Script","FSProg","G","Google Apps Script","Game Maker Language","GameMonkey Script","GAMS","GAP","G-code","Genie","GDL","Gibiane","GJ","GEORGE","GLSL","GNU E","GM","Go","Go!","GOAL","Gödel","Godiva","GOM (Good Old Mad)","Goo","Gosu","GOTRAN","GPSS","GraphTalk","GRASS","Groovy","Hack (programming language)","HAL/S","Hamilton C shell","Harbour","Hartmann pipelines","Haskell","Haxe","High Level Assembly","HLSL","Hop","Hope","Hugo","Hume","HyperTalk","IBM Basic assembly language","IBM HAScript","IBM Informix-4GL","IBM RPG","ICI","Icon","Id","IDL","Idris","IMP","Inform","Io","Ioke","IPL","IPTSCRAE","ISLISP","ISPF","ISWIM","J","J#","J++","JADE","Jako","JAL","Janus","JASS","Java","JavaScript","JCL","JEAN","Join Java","JOSS","Joule","JOVIAL","Joy","JScript","JScript .NET","JavaFX Script","Julia","Jython","K","Kaleidoscope","Karel","Karel++","KEE","Kixtart","KIF","Kojo","Kotlin","KRC","KRL","KUKA","KRYPTON","ksh","L","L# .NET","LabVIEW","Ladder","Lagoona","LANSA","Lasso","LaTeX","Lava","LC-3","Leda","Legoscript","LIL","LilyPond","Limbo","Limnor","LINC","Lingo","Linoleum","LIS","LISA","Lisaac","Lisp","Lite-C","Lithe","Little b","Logo","Logtalk","LPC","LSE","LSL","LiveCode","LiveScript","Lua","Lucid","Lustre","LYaPAS","Lynx","M2001","M4","Machine code","MAD","MAD/I","Magik","Magma","make","Maple","MAPPER","MARK-IV","Mary","MASM Microsoft Assembly x86","Mathematica","MATLAB","Maxima","Macsyma","Max","MaxScript","Maya (MEL)","MDL","Mercury","Mesa","Metacard","Metafont","MetaL","Microcode","MicroScript","MIIS","MillScript","MIMIC","Mirah","Miranda","MIVA Script","ML","Moby","Model 204","Modelica","Modula","Modula-2","Modula-3","Mohol","MOO","Mortran","Mouse","MPD","CIL","MSL","MUMPS","NASM","NATURAL","Napier88","Neko","Nemerle","nesC","NESL","Net.Data","NetLogo","NetRexx","NewLISP","NEWP","Newspeak","NewtonScript","NGL","Nial","Nice","Nickle","Nim","NPL","Not eXactly C","Not Quite C","NSIS","Nu","NWScript","NXT-G","o:XML","Oak","Oberon","Obix","OBJ2","Object Lisp","ObjectLOGO","Object REXX","Object Pascal","Objective-C","Objective-J","Obliq","Obol","OCaml","occam","occam-π","Octave","OmniMark","Onyx","Opa","Opal","OpenCL","OpenEdge ABL","OPL","OPS5","OptimJ","Orc","ORCA/Modula-2","Oriel","Orwell","Oxygene","Oz","P#","ParaSail (programming language)","PARI/GP","Pascal","Pawn","PCASTL","PCF","PEARL","PeopleCode","Perl","PDL","PHP","Phrogram","Pico","Picolisp","Pict","Pike","PIKT","PILOT","Pipelines","Pizza","PL-11","PL/0","PL/B","PL/C","PL/I","PL/M","PL/P","PL/SQL","PL360","PLANC","Plankalkül","Planner","PLEX","PLEXIL","Plus","POP-11","PostScript","PortablE","Powerhouse","PowerBuilder","PowerShell","PPL","Processing","Processing.js","Prograph","PROIV","Prolog","PROMAL","Promela","PROSE modeling language","PROTEL","ProvideX","Pro*C","Pure","Python","Q (equational programming language)","Q (programming language from Kx Systems)","Qalb","QtScript","QuakeC","QPL","R","R++","Racket","RAPID","Rapira","Ratfiv","Ratfor","rc","REBOL","Red","Redcode","REFAL","Reia","Revolution","rex","REXX","Rlab","RobotC","ROOP","RPG","RPL","RSL","RTL/2","Ruby","RuneScript","Rust","S","S2","S3","S-Lang","S-PLUS","SA-C","SabreTalk","SAIL","SALSA","SAM76","SAS","SASL","Sather","Sawzall","SBL","Scala","Scheme","Scilab","Scratch","Script.NET","Sed","Seed7","Self","SenseTalk","SequenceL","SETL","Shift Script","SIMPOL","SIGNAL","SiMPLE","SIMSCRIPT","Simula","Simulink","SISAL","SLIP","SMALL","Smalltalk","Small Basic","SML","Snap!","SNOBOL","SPITBOL","Snowball","SOL","Span","SPARK","Speedcode","SPIN","SP/k","SPS","Squeak","Squirrel","SR","S/SL","Stackless Python","Starlogo","Strand","Stata","Stateflow","Subtext","SuperCollider","SuperTalk","Swift (Apple programming language)","Swift (parallel scripting language)","SYMPL","SyncCharts","SystemVerilog","T","TACL","TACPOL","TADS","TAL","Tcl","Tea","TECO","TELCOMP","TeX","TEX","TIE","Timber","TMG","Tom","TOM","Topspeed","TPU","Trac","TTM","T-SQL","TTCN","Turing","TUTOR","TXL","TypeScript","Turbo C++","Ubercode","UCSD Pascal","Umple","Unicon","Uniface","UNITY","Unix shell","UnrealScript","Vala","VBA","VBScript","Verilog","VHDL","Visual Basic","Visual Basic .NET","Visual DataFlex","Visual DialogScript","Visual Fortran","Visual FoxPro","Visual J++","Visual J#","Visual Objects","Visual Prolog","VSXu","Vvvv","WATFIV, WATFOR","WebDNA","WebQL","Windows PowerShell","Winbatch","Wolfram","Wyvern","X++","X#","X10","XBL","XC","XMOS architecture","xHarbour","XL","Xojo","XOTcl","XPL","XPL0","XQuery","XSB","XSLT","XPath","Xtend","Yorick","YQL","Z notation","Zeno","ZOPL","ZPL"]
# Language list (short version)
LANGUAGES = ["Bash", "C", "C#", "C++", "Dart", "Go", "Java", "JavaScript", "Kotlin", "Lua", "MATLAB", "Perl", "PHP", "Python", "R", "Ruby", "Rust", "Scala", "Swift", "TypeScript"]


# Prepare data to be sent to Kafka
def build_repo_object(user: str, repo: str):
  content = {}
  content["user"] = user
  content["repo"] = repo
  content["languages"] = gr.get_languages(user, repo, headers=HEADERS)
  
  content["mainLanguage"] = list(content["languages"].keys())[0]
  content["readme"] = gr.get_readme(user, repo, headers=HEADERS)

  return content


# Handle progress
PROGRESS_FILE = 'saves/acquisition-progress.json'

def save_progress(language, page, processed_repos):
    progress = {
        'language': language,
        'page': page,
        'processed_repos': processed_repos
    }
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(progress, file)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as file:
                progress = json.load(file)
                print("Progress loaded.")
                return progress.get('language', LANGUAGES[0]), progress.get('page', 1), progress.get('processed_repos', [])
        except json.JSONDecodeError:
            print("Failed to decode progress file. Resetting progress.")
    else:
        print("No progress file found.")
    
    save_progress(LANGUAGES[0], 1, [])
    return LANGUAGES[0], 1, []

current_language, page, processed_repos = load_progress()

# Main loop
print("Starting main loop!")
while page <= 10: # Github only allows the first 1000 results
    for language in LANGUAGES:
        if language != current_language:
            continue

        try:
            results = gr.request_user_and_repo(language, page, headers=HEADERS)
        except Exception as e:
            print(f"Failed to request user and repo for language {language}: {e}")
            continue

        for user, repo in results:
            if (user, repo) in processed_repos:
                continue

            start_time = time.time()

            try:
                repo_object = build_repo_object(user, repo)
            except Exception as e:
                print(f"Failed to build repo object for {user}/{repo}: {e}")
                continue

            producer.send('new-git-repository', json.dumps(repo_object).encode('utf-8'))
            processed_repos.append((user, repo))
            save_progress(language, page, processed_repos)

            # Wait before the next request
            elapsed_time = time.time() - start_time
            if elapsed_time < wait_between_requests:
                time.sleep(wait_between_requests - elapsed_time)

        current_language = LANGUAGES[(LANGUAGES.index(language) + 1) % len(LANGUAGES)]
        save_progress(current_language, page, processed_repos)

    page += 1
    save_progress(current_language, page, processed_repos)