; Inno Setup Script for UpdatEngine-client
; Unpacked from original updatengine-client-setup and completed by Noël MARTINON
; The [Files] were generated with PyInstaller

#define MyAppName "UpdatEngine client"
#define MyAppVersion "2.4.9.4"
#define MyAppPublisher "UpdatEngine"
#define MyAppURL "http://www.updatengine.com"
#define MyAppSetupName "updatengine-client-setup"
#define MyAppSource "..\dist\updatengine-client"

[Setup]
AppId={{186C91F4-935B-4EEC-90B2-596F347AB706}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}/updatengine.ico
LicenseFile="{#MyAppSource}\LICENSE.txt"
OutputBaseFilename={#MyAppSetupName}-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "{#MyAppSource}\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\lxml._elementpath.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\lxml.etree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\Microsoft.VC90.CRT.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\msvcm90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\msvcp90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\msvcr90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\pywintypes27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\updatengine.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\updatengine-client.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\updatengine-client.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppSource}\win32pipe.pyd"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment\"; ValueName: "Path"; ValueType: ExpandSZ; ValueData: "{reg:HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\,Path};{app}"; Check: "NeedsAddPath(ExpandConstant('{app}'))"; MinVersion: 0.0,5.0; 

[Run]
Filename: "{cmd}"; Parameters: "/c copy /Y ""{code:GetCacert}"" ""{app}\cacert.pem"""; Check: "not CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine-monitor""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc ONSTART /tn ""Updatengine"" /tr "" \""{app}\updatengine-client.exe\"" -i {code:GetProxyOption} -s {code:GetServerAdress} -m {code:GetDelay} -c \""{app}\cacert.pem\"" -o \""{app}\updatengine-client.log\"" "" "; Check: "not CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc ONSTART /tn ""Updatengine"" /tr "" \""{app}\updatengine-client.exe\"" -i {code:GetProxyOption} -s {code:GetServerAdress} -m {code:GetDelay} -o \""{app}\updatengine-client.log\"" "" "; Check: "CheckEmptyCacert"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Create /ru ""SYSTEM"" /sc MINUTE /mo 10 /tn ""Updatengine-monitor"" /tr ""schtasks.exe /RUN /TN \""Updatengine\"" "" "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Run /tn ""Updatengine"" "" "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "sc.exe"; Parameters: " config schedule start= auto"; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Run /tn ""Updatengine""  "; Check: "CheckNoInstallInventory"; MinVersion: 0.0,5.0; Flags: runhidden;

[UninstallRun]
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine""  "; MinVersion: 0.0,5.0; Flags: runhidden;
Filename: "schtasks.exe"; Parameters: " /Delete /F /TN ""Updatengine-monitor""  "; MinVersion: 0.0,5.0; Flags: runhidden;

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
fr.NameAndVersion=%1 version %2
fr.AdditionalIcons=Icônes supplémentaires :
fr.CreateDesktopIcon=Créer une icône sur le &Bureau
fr.CreateQuickLaunchIcon=Créer une icône dans la barre de &Lancement rapide
fr.ProgramOnTheWeb=Page d'accueil de %1
fr.UninstallProgram=Désinstaller %1
fr.LaunchProgram=Exécuter %1
fr.AssocFileExtension=&Associer %1 avec l'extension de fichier %2
fr.AssocingFileExtension=Associe %1 avec l'extension de fichier %2...
fr.AutoStartProgramGroupDescription=Démarrage :
fr.AutoStartProgram=Démarrer automatiquement %1
fr.AddonHostProgramNotFound=%1 n'a pas été trouvé dans le dossier que vous avez choisi.%n%nVoulez-vous continuer malgré tout ?
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
en.ProxyHeader=By default (unchecked), UpdatEngine client will use Internet Explorer proxy settings.
en.ProxyBox=Check this box to disable Internet Explorer Proxy settings for Updatengine Client.
en.NoInstallInventoryTitle=Initial Inventory
en.NoInstallInventoryDescription=Launch inventory after Updatengine install
en.NoInstallInventoryHeader=By default (unchecked), UpdatEngine will launch an inventory after install.
en.NoInstallInventory= Check this box to disable UpdatEngine inventory after install.
fr.TitleConfiguration=Configuration du client UpdatEngine
fr.SubTitleConfiguration=Configuration de l'adresse du serveur et des délais d'inventaires
fr.TipsConfiguration=Saisissez dans les deux champs suivants l'adresse du serveur UpdatEngine et le délais d'inventaire
fr.Server=Adresse (http ou https) du serveur UpdatEngine
fr.Delay=Délais d'attente entre deux inventaires (en minutes)
fr.UrlValue=https://votre_serveur_updatengine:1979
fr.SslCertificate=Certificat SSL
fr.SslTips=Choisissez le certificat SSL propre à ce serveur
fr.SslWarning=Attention: Sans certificat de sécurité, votre client sera vulnérable à une attaque de type MITM. Référez-vous à la documentation du client pour plus d'informations
fr.SslField=Choisissez ici le certificat SSL de votre serveur Web.
fr.ProxyTitle=Paramètres de proxy
fr.ProxyDescription=Utilisation du proxy Internet Explorer pour le client UpdatEngine
fr.ProxyHeader=Par défaut (case décochée), le client UpdatEngine utilisera les paramètres du proxy Internet Explorer.
fr.ProxyBox=Cochez cette case pour ne pas utiliser le Proxy déclaré dans Internet Explorer
fr.NoInstallInventoryTitle=Inventaire intial
fr.NoInstallInventoryDescription=Lancement d'un inventaire après installation
fr.NoInstallInventoryHeader=Par défaut (case décochée), le client UpdatEngine lancera un inventaire dès la fin d'installation.
fr.NoInstallInventory= Cochez cette case pour ne pas lancer d'inventaire après l'installation
en.AllFiles=All files
en.PemFiles=PEM SSL Certificat
fr.AllFiles=Tous les fichiers
fr.PemFiles=Certificat SSL PEM
en.SslCertError=File does not exist or is emtpy. Please select the correct file.
fr.SslCertError=Le fichier n'existe pas ou est vide. Veuillez sélectionner un fichier correct.

[Code]
var    
  ConfigPage: TInputQueryWizardPage;
  InventoryPage: TInputOptionWizardPage;
  ProxyPage: TInputOptionWizardPage;
  SslCertificatePage: TInputFileWizardPage;

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

  { Inventory page }
  InventoryPage := CreateInputOptionPage(ConfigPage.ID,
    expandConstant('{cm:NoInstallInventoryTitle}'), expandConstant('{cm:NoInstallInventoryDescription}'),
    expandConstant('{cm:NoInstallInventoryHeader}'),
    False, False);
  InventoryPage.Add(expandConstant('{cm:NoInstallInventory}'));
  
  if GetPreviousData('NoInstallInventory', '') = 'True' then
    InventoryPage.Values[0] := True;

  { Proxy page }
  ProxyPage := CreateInputOptionPage(InventoryPage.ID,
    expandConstant('{cm:ProxyTitle}'), expandConstant('{cm:ProxyDescription}'),
    expandConstant('{cm:ProxyHeader}'),
    False, False);
  ProxyPage.Add(expandConstant('{cm:ProxyBox}'));

  if GetPreviousData('ProxyBox', '') = 'True' then
    ProxyPage.Values[0] := True;

  { Certificate page }
  SslCertificatePage := CreateInputFilePage(ProxyPage.ID,
    expandConstant('{cm:SslCertificate}'), expandConstant('{cm:SslTips}'),
    expandConstant('{cm:SslWarning}'));  
  SslCertificatePage.Add(expandConstant('{cm:SslField}'),
    expandConstant('{cm:PemFiles}|*.pem|{cm:AllFiles}|*.*'), '.pem');

  SslCertificatePage.Values[0] := GetPreviousData('SslField', '');
end;

// --------------------------------
// Store the settings so we can restore them next time
procedure RegisterPreviousData(PreviousDataKey: Integer);
begin  
  SetPreviousData(PreviousDataKey, 'Server', ConfigPage.Values[0]);
  SetPreviousData(PreviousDataKey, 'Delay', ConfigPage.Values[1]);
  if InventoryPage.Values[0] = True then
    SetPreviousData(PreviousDataKey, 'NoInstallInventory', 'True');
  if ProxyPage.Values[0] = True then
    SetPreviousData(PreviousDataKey, 'ProxyBox', 'True');
  SetPreviousData(PreviousDataKey, 'SslField', SslCertificatePage.Values[0]);
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
    Result := '/noproxy';
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
// Check if inventory is launched after installation
function CheckNoInstallInventory: Boolean;
begin
  if not InventoryPage.Values[0] then
    Result := True;
end; 

// --------------------------------
// Check if certificat file is empty
function CheckEmptyCacert: Boolean;
var
  Size: Integer;
begin       
    if not FileSize(SslCertificatePage.Values[0], Size) or (Size = 0) then
      Result := True;
end;

// --------------------------------
// Check certificat file on next button click
function NextButtonClick(PageId: Integer): Boolean;
begin
    Result := True;
    if (PageId = SslCertificatePage.ID) and (SslCertificatePage.Values[0]<>'') and CheckEmptyCacert then begin
        MsgBox(expandConstant('{cm:SslCertError}'), mbError, MB_OK);
        Result := False;
        exit;
    end;
end;
