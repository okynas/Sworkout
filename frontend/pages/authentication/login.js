import Head from 'next/head'
import Image from 'next/image'
import Footer from '../../components/Footer'
import Header from '../../components/Header'

export default function Login() {
  return (
    <>
      <Header/>

      <main className="container my-10 mx-auto">
        <section className="prose text-text">
          <h1 className="text-text text-2xl">login</h1>

        </section>
      </main>

      <Footer/>
    </>
  )
};