; Inno Setup Script for UpdatEngine-client
; Unpacked from original updatengine-client-setup and completed by No�l MARTINON
; The [Files] were generated with PyInstaller
;
; Specific command line arguments : server, delay, cert, noproxy, noinventorynow, nolog, forceinstall
;

#define MyAppName "UpdatEngine client"
#define MyAppVersion "4.1.3"
#define MyAppPublisher "UpdatEngine-NG"
#define MyAppURL "https://github.com/updatengine-ng/updatengine-client"
#define MyAppSetupName "updatengine-client-setup"
#define MyAppSource "..\dist\updatengine-client"

[Setup]
AppId={{74B4EB48-7DE3-4708-B36D-7D40F1426658}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppCopyright=Copyright (C) 2021 {#MyAppPublisher}
VersionInfoVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf}\{#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\updatengine.ico
LicenseFile="{#MyAppSource}\LICENSE.txt"
OutputBaseFilename={#MyAppSetupName}-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "{#MyAppSource}\_bz2.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion; BeforeInstall: CheckForceInstall()
Source: "{#MyAppSource}\_ctypes.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\_hashlib.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\_lzma.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\_socket.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\_ssl.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\_win32sysloader.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-console-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-datetime-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-debug-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-errorhandling-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-file-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-file-l1-2-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-file-l2-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-handle-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-interlocked-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-libraryloader-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-localization-l1-2-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-memory-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-namedpipe-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-processenvironment-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-processthreads-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-processthreads-l1-1-1.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-profile-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-rtlsupport-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-string-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-synch-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-synch-l1-2-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-sysinfo-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-timezone-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-core-util-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-conio-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-convert-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-environment-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-filesystem-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-locale-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-math-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-multibyte-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-process-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-runtime-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-stdio-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-string-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-time-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\api-ms-win-crt-utility-l1-1-0.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\base_library.zip"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\libcrypto-1_1.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\libssl-1_1.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\LICENSE.txt"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\mfc140u.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\pyexpat.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\python37.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\pythoncom37.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\pywintypes37.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\select.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\ucrtbase.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\unicodedata.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\updatengine-client.exe"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\updatengine-client.exe.manifest"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\updatengine.ico"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\win32api.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\win32trace.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\win32ui.pyd"; DestDir: "{app}"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\lxml\_elementpath.cp37-win32.pyd"; DestDir: "{app}\lxml"; Flags: restartreplace ignoreversion
Source: "{#MyAppSource}\lxml\etree.cp37-win32.pyd"; DestDir: "{app}\lxml"; Flags: restartreplace ignoreversion

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment\"; ValueName: "Path"; ValueType: ExpandSZ; ValueData: "{reg:HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\,Path};{app}"; Check: "NeedsAddPath(ExpandConstant('{app}'))"; MinVersion: 0.0,5.0;

[Run]
Filename: "{cmd}"; Parameters: "/c copy /Y ""{code:GetCacert}"" ""{app}\cacert.pem"""; Check: "not CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine-monitor""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc ONSTART /tn ""Updatengine"" /tr "" \""{app}\updatengine-client.exe\"" -i {code:GetProxyOption} -s {code:GetServerAdress} -m {code:GetDelay} -c \""{app}\cacert.pem\"" {code:GetLogging} "" "; Check: "not CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc ONSTART /tn ""Updatengine"" /tr "" \""{app}\updatengine-client.exe\"" -i {code:GetProxyOption} -s {code:GetServerAdress} -m {code:GetDelay} {code:GetLogging} "" "; Check: "CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc MINUTE /mo 10 /tn ""Updatengine-monitor"" /tr ""schtasks.exe /Run /tn \""Updatengine\"" "" "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "sc.exe"; Parameters: " config schedule start= auto"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Run /tn ""Updatengine"" "; Check: "CheckNoInstallInventory"; MinVersion: 0.0,5.0; Flags: runhidden;

[UninstallRun]
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine-monitor""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "taskkill.exe"; Parameters: " /f /t /im updatengine-client.exe"; Flags: runhidden
Filename: "ping.exe"; Parameters: "127.0.0.1 -n 1"; Flags: runhidden

[UninstallDelete]
Type: filesandordirs; Name: "{app}";

[CustomMessages]
en.NameAndVersion=%1 version %2
en.AdditionalIcons=Additional shortcuts:
en.CreateDesktopIcon=Create a &desktop shortcut
en.CreateQuickLaunchIcon=Create a &Quick Launch shortcut
en.ProgramOnTheWeb=%1 on the Web
en.UninstallProgram=Uninstall %1
en.LaunchProgram=Launch %1
en.AssocFileExtension=&Associate %1 with the %2 file extension
en.AssocingFileExtension=Associating %1 with the %2 file extension...
en.AutoStartProgramGroupDescription=Startup:
en.AutoStartProgram=Automatically start %1
en.AddonHostProgramNotFound=%1 could not be located in the folder you selected.%n%nDo you want to continue anyway?
en.TitleConfiguration=UpdatEngine client configuration
en.SubTitleConfiguration=Configure UpatdEngine server adress and delay
en.TipsConfiguration=Please enter your UpdatEngine''s server adress and the delay between each inventory (in minutes)
en.Server=Updatengine server url
en.Delay=Delay between each inventory (minutes)
en.UrlValue=https://your_updatengine_server:1979
en.SslCertificate=SSL certificate
en.SslTips=Select your cacert.pem file if needed
en.SslWarning=Warning: without selecting a cacert.pem file, your installation will vulnerable to MITM attacks. For more information, please consult updatengine client documentation
en.SslField=Select your webserver's SSL certificate
en.ProxyTitle=Proxy configuration
en.ProxyDescription=Use or not system proxy
en.ProxyHeader=By default (unchecked), UpdatEngine client will use internet proxy settings.
en.ProxyBox=Check this box to disable internet proxy settings for Updatengine Client.
en.NoInstallInventoryTitle=Initial Inventory
en.NoInstallInventoryDescription=Launch inventory after Updatengine install
en.NoInstallInventoryHeader=By default (unchecked), UpdatEngine will launch an inventory after install.
en.NoInstallInventoryBox=Check this box to disable UpdatEngine inventory after install.
en.AllFiles=All files
en.PemFiles=PEM SSL Certificat
en.SslCertError=File does not exist or is emtpy. Please select the correct file.
en.LogTitle=Event log
en.LogDescription=Log of the application activity
en.LogHeader=By default (unchecked), UpdatEngine Client logs its activity in its installation directory.
en.LogBox=Check this box to disable UpdatEngine Client logging
fr.NameAndVersion=%1 version %2
fr.AdditionalIcons=Ic�nes suppl�mentaires :
fr.CreateDesktopIcon=Cr�er une ic�ne sur le &Bureau
fr.CreateQuickLaunchIcon=Cr�er une ic�ne dans la barre de &Lancement rapide
fr.ProgramOnTheWeb=Page d'accueil de %1
fr.UninstallProgram=D�sinstaller %1
fr.LaunchProgram=Ex�cuter %1
fr.AssocFileExtension=&Associer %1 avec l'extension de fichier %2
fr.AssocingFileExtension=Associe %1 avec l'extension de fichier %2...
fr.AutoStartProgramGroupDescription=D�marrage :
fr.AutoStartProgram=D�marrer automatiquement %1
fr.AddonHostProgramNotFound=%1 n'a pas �t� trouv� dans le dossier que vous avez choisi.%n%nVoulez-vous continuer malgr� tout ?
fr.TitleConfiguration=Configuration du client UpdatEngine
fr.SubTitleConfiguration=Configuration de l'adresse du serveur et des d�lais d'inventaires
fr.TipsConfiguration=Saisissez dans les deux champs suivants l'adresse du serveur UpdatEngine et le d�lais d'inventaire
fr.Server=Adresse (http ou https) du serveur UpdatEngine
fr.Delay=D�lais d'attente entre deux inventaires (en minutes)
fr.UrlValue=https://votre_serveur_updatengine:1979
fr.SslCertificate=Certificat SSL
fr.SslTips=Choisissez le certificat SSL propre � ce serveur
fr.SslWarning=Attention: Sans certificat de s�curit�, votre client sera vuln�rable � une attaque de type MITM. R�f�rez-vous � la documentation du client pour plus d'informations
fr.SslField=Choisissez ici le certificat SSL de votre serveur Web.
fr.ProxyTitle=Param�tres de proxy
fr.ProxyDescription=Utilisation du proxy internet du syst�me pour le client UpdatEngine
fr.ProxyHeader=Par d�faut (case d�coch�e), le client UpdatEngine utilisera les param�tres du proxy d�finis dans les options internet du syst�me.
fr.ProxyBox=Cochez cette case pour ne pas utiliser le proxy internet du syst�me
fr.NoInstallInventoryTitle=Inventaire intial
fr.NoInstallInventoryDescription=Lancement d'un inventaire apr�s installation
fr.NoInstallInventoryHeader=Par d�faut (case d�coch�e), le client UpdatEngine lancera un inventaire d�s la fin d'installation.
fr.NoInstallInventoryBox=Cochez cette case pour ne pas lancer d'inventaire apr�s l'installation
fr.AllFiles=Tous les fichiers
fr.PemFiles=Certificat SSL PEM
fr.SslCertError=Le fichier n'existe pas ou est vide. Veuillez s�lectionner un fichier correct.
fr.LogTitle=Journal d'�v�nements
fr.LogDescription=Enregitrement de l'activit� de l'application
fr.LogHeader=Par d�faut (case d�coch�e), le client UpdatEngine enregitrera ses �venements dans le r�pertoire d'installation.
fr.LogBox=Cochez cette case pour d�sactiver la journalisation du client UpdatEngine

[Code]
var
  ConfigPage: TInputQueryWizardPage;
  InventoryPage: TInputOptionWizardPage;
  ProxyPage: TInputOptionWizardPage;
  SslCertificatePage: TInputFileWizardPage;
  LogPage: TInputOptionWizardPage;

// Define function prototype
function CmdLineParamExists(const Value: string): Boolean; forward;

// --------------------------------
// Wizard initialization : Create the pages
procedure InitializeWizard;
begin
  { Config page }
  ConfigPage := CreateInputQueryPage(wpLicense,
    expandConstant('{cm:TitleConfiguration}'), ExpandConstant('{cm:SubTitleConfiguration}'),
    expandConstant('{cm:TipsConfiguration}'));
  ConfigPage.Add(expandConstant('{cm:Server}'), False);
  ConfigPage.Add(expandConstant('{cm:Delay}'), False);

  ConfigPage.Values[0] := GetPreviousData('Server', ExpandConstant('{cm:UrlValue}'));
  ConfigPage.Values[1] := GetPreviousData('Delay', '30');

  if length(ExpandConstant('{param:server}')) > 0 then
    ConfigPage.Values[0] := ExpandConstant('{param:server}');
  if StrToInt(ExpandConstant('{param:delay|0}')) > 0 then
    ConfigPage.Values[1] := ExpandConstant('{param:delay}');

  { Certificate page }
  SslCertificatePage := CreateInputFilePage(ConfigPage.ID,
    expandConstant('{cm:SslCertificate}'), expandConstant('{cm:SslTips}'),
    expandConstant('{cm:SslWarning}'));
  SslCertificatePage.Add(expandConstant('{cm:SslField}'),
    expandConstant('{cm:PemFiles}|*.pem|{cm:AllFiles}|*.*'), '.pem');

  SslCertificatePage.Values[0] := GetPreviousData('SSLcertificat', '');

  if length(ExpandConstant('{param:cert}')) > 0 then
    SslCertificatePage.Values[0] := ExpandConstant('{param:cert}')
  else if ParamCount > 1 then
    SslCertificatePage.Values[0] := '';

  { Inventory page }
  InventoryPage := CreateInputOptionPage(SslCertificatePage.ID,
    expandConstant('{cm:NoInstallInventoryTitle}'), expandConstant('{cm:NoInstallInventoryDescription}'),
    expandConstant('{cm:NoInstallInventoryHeader}'),
    False, False);
  InventoryPage.Add(expandConstant('{cm:NoInstallInventoryBox}'));

  if GetPreviousData('NoInstallInventory', '') = 'True' then
    InventoryPage.Values[0] := True;

  if CmdLineParamExists('/noinventorynow') = True then
    InventoryPage.Values[0] := True
  else if ParamCount > 1 then
    InventoryPage.Values[0] := False;

  { Proxy page }
  ProxyPage := CreateInputOptionPage(InventoryPage.ID,
    expandConstant('{cm:ProxyTitle}'), expandConstant('{cm:ProxyDescription}'),
    expandConstant('{cm:ProxyHeader}'),
    False, False);
  ProxyPage.Add(expandConstant('{cm:ProxyBox}'));

  if GetPreviousData('NoProxy', '') = 'True' then
    ProxyPage.Values[0] := True;

  if CmdLineParamExists('/noproxy') = True then
    ProxyPage.Values[0] := True
  else if ParamCount > 1 then
    ProxyPage.Values[0] := False;

  { Log page }
  LogPage := CreateInputOptionPage(ProxyPage.ID,
    expandConstant('{cm:LogTitle}'), expandConstant('{cm:LogDescription}'),
    expandConstant('{cm:LogHeader}'),
    False, False);
  LogPage.Add(expandConstant('{cm:LogBox}'));

  if GetPreviousData('NoLogging', '') = 'True' then
    LogPage.Values[0] := True;

  if CmdLineParamExists('/nolog') = True then
    LogPage.Values[0] := True
  else if ParamCount > 1 then
    LogPage.Values[0] := False;

end;

// --------------------------------
// Store the settings so we can restore them next time
procedure RegisterPreviousData(PreviousDataKey: Integer);
begin
  SetPreviousData(PreviousDataKey, 'Server', ConfigPage.Values[0]);
  SetPreviousData(PreviousDataKey, 'Delay', ConfigPage.Values[1]);
  if (Pos('https://',LowerCase(ConfigPage.Values[0])) = 1) then
    SetPreviousData(PreviousDataKey, 'SSLcertificat', SslCertificatePage.Values[0])
  else SetPreviousData(PreviousDataKey, 'SSLcertificat', '');
  if InventoryPage.Values[0] = True then
    SetPreviousData(PreviousDataKey, 'NoInstallInventory', 'True');
  if ProxyPage.Values[0] = True then
    SetPreviousData(PreviousDataKey, 'NoProxy', 'True');
  if LogPage.Values[0] = True then
    SetPreviousData(PreviousDataKey, 'NoLogging', 'True');
end;

// --------------------------------
// Check if certificat page is shown or skipped
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False; //not necessary, but safer
  if (PageID = SslCertificatePage.ID) and
     (Pos('https://',LowerCase(ConfigPage.Values[0])) <> 1) then
    Result := true;
end;

// --------------------------------
// Check if it is needed to add '{app}' path to registry
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  // look for the path with leading and trailing semicolon
  Result := Pos(';' + UpperCase(Param) + ';', ';' + UpperCase(OrigPath) + ';') = 0;
  if Result = True then
    Result := Pos(';' + UpperCase(Param) + '\;', ';' + UpperCase(OrigPath) + ';') = 0;
end;

// --------------------------------
// Get certificat file string
function GetCacert(Value: string): string;
begin
  Result := SslCertificatePage.Values[0];
end;

// --------------------------------
// Get proxy use option
function GetProxyOption(Value: string): string;
begin
  if ProxyPage.Values[0] then
    Result := '-n';
end;

// --------------------------------
// Get server string
function GetServerAdress(Value: string): string;
begin
  Result := ConfigPage.Values[0];
end;

// --------------------------------
// Get delay value
function GetDelay(Value: string): string;
begin
  Result := ConfigPage.Values[1];
end;

// --------------------------------
// Get logging value
function GetLogging(Value: string): string;
begin
  if not LogPage.Values[0] then
    Result := ExpandConstant('-o \"{app}\updatengine-client.log\"');
end;

// --------------------------------
// Check if inventory is launched after installation
function CheckNoInstallInventory: Boolean;
var
  ResultCode: Integer;
begin
  if not InventoryPage.Values[0] then
    Exec(ExpandConstant('{sys}\schtasks.exe'), '/Run /tn "Updatengine"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Result := True;
end;

// --------------------------------
// Check if certificat file is empty
// -> The response is always 'True' if server url is not https
function CheckEmptyCacert: Boolean;
var
  Size: Integer;
begin
  if (not FileSize(SslCertificatePage.Values[0], Size) or (Size = 0)) or (Pos('https://',LowerCase(ConfigPage.Values[0])) <> 1) then
    Result := True;
end;

// --------------------------------
// Check certificat file on next button click
function NextButtonClick(PageId: Integer): Boolean;
begin
  Result := True;
  if (PageId = SslCertificatePage.ID) and (SslCertificatePage.Values[0]<>'') and CheckEmptyCacert then begin
    if ParamCount = 1 then
      MsgBox(expandConstant('{cm:SslCertError}'), mbError, MB_OK);
    Result := False;
    exit;
  end;
end;

// --------------------------------
// Kill a Win32 process
procedure TaskKill(FileName: String);
var
  ResultCode: Integer;
begin
  Exec('taskkill.exe', '/f /t /im ' + '"' + FileName + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

// --------------------------------
// Check if command line parameter exists
function CmdLineParamExists(const Value: string): Boolean;
var
  I: Integer;
begin
  Result := False;
  for I := 1 to ParamCount do
    if CompareText(ParamStr(I), Value) = 0 then
    begin
      Result := True;
      Break;
    end;
end;

// --------------------------------
// Stop previous running application if parameter is specified
procedure CheckForceInstall();
begin
  if CmdLineParamExists('/forceinstall') = True then
    TaskKill('updatengine-client.exe');
end;

// --------------------------------

