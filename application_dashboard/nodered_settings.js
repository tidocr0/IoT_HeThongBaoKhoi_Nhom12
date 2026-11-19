/**
 * Cau hinh Node-RED chuan da may (Portable) - Nhom 12 (IT4735)
 * Dam bao tat ca thanh vien pull Git ve deu chay giong nhau khong le thuoc settings rieng.
 */
module.exports = {
    credentialSecret: false,
    flowFilePretty: true,
    uiPort: process.env.PORT || 1880,
    functionGlobalContext: {},
    functionExternalModules: true,
    externalModules: {
        palette: {
            allowInstall: true
        }
    },
    logging: {
        console: {
            level: "info",
            metrics: false,
            audit: false
        }
    },
    editorTheme: {
        projects: {
            enabled: false
        }
    }
};
