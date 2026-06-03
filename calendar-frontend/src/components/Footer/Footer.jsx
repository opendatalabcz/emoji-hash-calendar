import "./Footer.css";

function Footer() {
    return (
        <footer className="footer">
            <p className="footer-text">
                Tento projekt vznikl jako bakalářská práce na{" "}
                <a href="https://fit.cvut.cz" target="_blank" rel="noopener noreferrer">
                    FIT ČVUT
                </a>
            </p>

            <p className="footer-disclaimer">
                Provozovatel neodpovídá za správnost a úplnost zpracovaných dat a informací,
                ani tato neověřuje a zříká se zodpovědnosti za veškeré škody a újmy,
                které by použitím těchto dat mohly vzniknout.
            </p>

            <div className="footer-logos">
                <a href="https://opendatalab.cz/" target="_blank" rel="noopener noreferrer">
                    <img src="/opendatalab.svg" alt="OpenDataLab" />
                </a>

                <a href="https://fit.cvut.cz/cs" target="_blank" rel="noopener noreferrer">
                    <img src="/fit-cvut-logo.svg" alt="FIT ČVUT" />
                </a>

                <a href="https://profinit.eu/" target="_blank" rel="noopener noreferrer">
                    <img src="/profinit.svg" alt="Profinit" />
                </a>
            </div>
        </footer>
    );
}

export default Footer;
