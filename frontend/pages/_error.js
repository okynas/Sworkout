import Footer from "../components/Footer"
import Header from "../components/Header"

function Error({ statusCode }) {
  return (
    <>
      <Header/>

      <main className="container my-10 mx-auto">
        <article className="prose text-text">
          <h1 className="text-text text-2xl">Oisann</h1>
          <p className="font-bold text-text">
            {statusCode
              ? statusCode == 404
                ? `Vi fant ikke siden du leter etter`
                : `Det er noe rusk i maskineriet, feilkode: ${statusCode}`
              : 'En uventet feil oppsto'
            }
          </p>
          <p className="text-text">
            Hvis du er sikker på at nettadressen er riktig, <br/>
            kontakt oss på <a href="mailto:post@sworkout.com">post@sworkout.com</a>
          </p>
        </article>
      </main>

      <Footer/>
    </>
  )
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404
  return { statusCode }
}

export default Error