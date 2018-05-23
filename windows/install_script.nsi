;NSIS Script Installer for Pireal
#######################################################################
# Startup
!define VERSION "3.0"
!define NAME "Pireal ${VERSION}"
!define DISPLAY_NAME "Pireal ${VERSION}"
!define WEB_SITE "http://centaurialpha.github.io/pireal"
!define FINALNAME "pireal-${VERSION}-installer.exe"

!include "MUI2.nsh"
Unicode true
#######################################################################
# Attributes

Name "${DISPLAY_NAME}"
OutFile "${FINALNAME}"
Caption "${DISPLAY_NAME}"

LicenseData "COPYING"
InstallDir $PROGRAMFILES\Pireal

######################################################################
# Interface Settings

ShowInstDetails show
AutoCloseWindow false
SilentInstall normal
CRCCheck on
SetCompressor /SOLID /FINAL lzma
SetDatablockOptimize on
SetOverwrite try
XPStyle on

######################################################################
# Pages

!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_ABORTWARNING
!define MUI_LANGDLL_ALLLANGUAGES
!define MUI_FINISHPAGE_RUN "$INSTDIR\pireal.exe"
!define MUI_FINISHPAGE_NOREBOOTSUPPORT
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "sidebar.bmp"
!define MUI_LICENSEPAGE

!insertmacro MUI_PAGE_LICENSE "COPYING"
# !insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

#!define MUI_COMPONENTSPAGE_SMALLDESC
#!define MUI_COMPONENTSPAGE_NODESC

# !insertmacro MUI_PAGE_WELCOME
# !insertmacro MUI_PAGE_COMPONENTS

# !insertmacro MUI_UNPAGE_WELCOME

######################################################################
# Languages

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Bulgarian"
!insertmacro MUI_LANGUAGE "Catalan"
!insertmacro MUI_LANGUAGE "Croatian"
!insertmacro MUI_LANGUAGE "Czech"
!insertmacro MUI_LANGUAGE "Danish"
!insertmacro MUI_LANGUAGE "Dutch"
!insertmacro MUI_LANGUAGE "Estonian"
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Greek"
!insertmacro MUI_LANGUAGE "Hungarian"
!insertmacro MUI_LANGUAGE "Italian"
!insertmacro MUI_LANGUAGE "Korean"
!insertmacro MUI_LANGUAGE "Latvian"
!insertmacro MUI_LANGUAGE "Norwegian"
!insertmacro MUI_LANGUAGE "Polish"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "Slovak"
!insertmacro MUI_LANGUAGE "Slovenian"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Swedish"
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "Ukrainian"

!insertmacro MUI_RESERVEFILE_LANGDLL

InstallDirRegKey HKLM "Software\Pireal" ""

Section "Pireal core"
  SectionIn RO
  SetOutPath "$INSTDIR"
  File /r "build\"
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\${NAME}"
  CreateShortcut "$SMPROGRAMS\${NAME}\${NAME}.lnk" "$INSTDIR\${NAME}.exe"
  CreateShortcut "$DESKTOP\${NAME}.lnk" "$INSTDIR\${NAME}.exe"
  CreateShortcut "$SMPROGRAMS\${NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${NAME} "DisplayName" "${NAME} ${VERSION}"
  WriteRegStr HKLM SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${NAME} "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteUninstaller "Uninstall.exe"
  WriteRegStr HKLM SOFTWARE\${NAME} "InstallDir" $INSTDIR
  WriteRegStr HKLM SOFTWARE\${NAME} "Version" "${VERSION}"
SectionEnd

#Section /o "Samples"
#  SetOutPath "$DOCUMENTS\${NAME}_samples"
  # File /r "samples\"
#  CreateDirectory "$DOCUMENTS\${NAME}_samples"
#SectionEnd

######################################################################
# Functions, utilities

Function .onInit
  SetOutPath $TEMP
  File /oname=spltmp.bmp "splash.bmp"
  splash::show 2300 $TEMP\spltmp
  Pop $0
  Delete $TEMP\spltmp.bmp
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

######################################################################
# Uninstall

UninstallText "This program will uninstall Pireal, continue?"
ShowUninstDetails show

Section "Uninstall"
  SetShellVarContext all
  RMDir /r "$SMPROGRAMS\${NAME}"
  RMDir /r "$INSTDIR\${NAME}"
  Delete "$DESKTOP\${NAME}.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKLM SOFTWARE\${NAME}
  DeleteRegKey HKLM Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}
SectionEnd
