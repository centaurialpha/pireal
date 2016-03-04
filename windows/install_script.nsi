!define PRODUCT_NAME "Pireal"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Gabriel Acosta"
!define PRODUCT_WEB_SITE "http://centaurialpha.github.io/pireal"

!include "MUI2.nsh"
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}_setup.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"

!define MUI_ABORTWARNING
