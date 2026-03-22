; ============================================================
; ApT — Áudio para Texto
; Script Inno Setup v1.0.0
; ============================================================

#define AppName      "ApT"
#define AppVersion   "1.0.0"
#define AppPublisher "Brunno ML"
#define AppURL       "https://www.brunnoml.com.br/produtos/apt"
#define AppExeName   "ApT.exe"
#define SourceDir    "C:\Users\BrunnoML\Documents\apt\dist\ApT"
#define IconFile     "C:\Users\BrunnoML\Documents\apt\images\apt.ico"

[Setup]
AppId={{A7F3C2D1-4E8B-4F9A-BC6D-1234567890AB}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
OutputDir=C:\Users\BrunnoML\Documents\apt\installer
OutputBaseFilename=ApT-Setup-v{#AppVersion}
SetupIconFile={#IconFile}
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\ApT.exe";         DestDir: "{app}";           Flags: ignoreversion
Source: "{#SourceDir}\_internal\*";     DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName} — Áudio para Texto"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\{#AppExeName}"
Name: "{group}\Desinstalar {#AppName}";         Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}";               Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Executar {#AppName} agora"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
