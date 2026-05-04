(function() {
        const RELEASES_URL =
                "https://github.com/centaurialpha/pireal/releases/latest";

        const STRINGS = {
                es: {
                        windows: "Descargar para Windows",
                        linux: "Descargar para Linux",
                        mac: "Ver instrucciones (macOS)",
                        other: "Descargar",
                        getstarted: "Primeros pasos",
                        license: "Libre y de código abierto",
                        subtitle: 'Un intérprete de <strong>Álgebra Relacional</strong> para aprender bases de datos desde cero.',
                        desc: "Escribí consultas, explorá resultados, visualizá el árbol de sintaxis y generá SQL equivalente, sin instalar un motor de base de datos.",
                },
                en: {
                        windows: "Download for Windows",
                        linux: "Download for Linux",
                        mac: "See instructions (macOS)",
                        other: "Download",
                        getstarted: "Get started",
                        license: "Free and open source",
                        subtitle: 'A <strong>Relational Algebra</strong> interpreter for learning databases from the ground up.',
                        desc: "Write queries, explore results, visualize the syntax tree and generate equivalent SQL, without installing a database engine.",
                },
        };

        const OS_ASSET = {
                windows: /pireal.*\.exe$/i,
                linux: /Pireal.*\.AppImage$/i,
        };

        function detectLang() {
                const lang = document.documentElement.lang || "en";
                return lang.startsWith("en") ? "en" : "es";
        }

        function detectOS() {
                const ua = navigator.userAgent.toLowerCase();
                const pf = (navigator.platform || "").toLowerCase();
                if (pf.includes("win") || ua.includes("windows")) return "windows";
                if (pf.includes("linux") || ua.includes("linux")) return "linux";
                if (pf.includes("mac") || ua.includes("mac")) return "mac";
                return "other";
        }

        async function resolveDownloadURL(os) {
                const pattern = OS_ASSET[os];
                if (!pattern) return RELEASES_URL;
                try {
                        const res = await fetch(
                                "https://api.github.com/repos/centaurialpha/pireal/releases/latest",
                                { headers: { Accept: "application/vnd.github+json" } }
                        );
                        if (!res.ok) return RELEASES_URL;
                        const data = await res.json();
                        const asset = (data.assets || []).find((a) => pattern.test(a.name));
                        return asset?.browser_download_url ?? RELEASES_URL;
                } catch {
                        return RELEASES_URL;
                }
        }

        function setText(id, html) {
                const el = document.getElementById(id);
                if (el) el.innerHTML = html;
        }

        async function init() {
                const lang = detectLang();
                const os = detectOS();
                const t = STRINGS[lang];

                setText("pi-subtitle", t.subtitle);
                setText("pi-desc", t.desc);
                setText("pi-getstarted-text", t.getstarted);
                setText("pi-license-text", t.license);
                setText("pi-download-text", t[os] || t.other);

                const btn = document.getElementById("pi-download-btn");
                if (!btn) return;

                if (os === "mac") { btn.href = "getting-started/"; return; }
                if (os === "other") { btn.href = RELEASES_URL; return; }

                btn.href = await resolveDownloadURL(os);
        }

        if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", init);
        } else {
                init();
        }
})();
