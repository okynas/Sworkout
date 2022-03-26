import Image from 'next/image'
import Link from 'next/link';

export default function Footer({className}) {
  return (
    <footer className={`p-4 sm:p-6 dark:bg-gray-800 container mx-auto ${className}`}>
      <hr className="my-6 opacity-10 border-text sm:mx-auto dark:border-gray-700 lg:my-8 w-full" />
      <div className="md:flex md:justify-between">
        <div className="mb-6 md:mb-0">
          <Link href="/">
            <a className="h-10 flex flex-row items-center hover:text-gray-300">
              <Image src="/assets/logos/logo.png" alt="Trenger AS logo" width={50} height={50} />
              <span className='font-thin leading-tight'>SWorkout</span>
            </a>
          </Link>
          <span className="block mt-3 text-sm text-text dark:text-gray-400">
            &copy; 2022 Trenger AS. Org. 928 050 106
          </span>
        </div>
          <div className="grid grid-cols-2 gap-8 sm:gap-6 sm:grid-cols-3">
            <div>
              <h2 className="mb-6 text-sm font-semibold text-text uppercase dark:text-white">
                Snarveier
              </h2>
              <ul>
                <li className="mb-4">
                  <Link href="/account">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Min side
                    </a>
                  </Link>
                </li>
                <li>
                  <Link href="/account/orders" rel="nofollow">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Ordreoversikt
                    </a>
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h2 className="mb-6 text-sm font-semibold text-text uppercase dark:text-white">
                Informasjon
              </h2>
              <ul>
                <li className="mb-4">
                  <Link href="/about/terms">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Utleiebetingelser
                    </a>
                  </Link>
                </li>
                <li>
                  <Link href="/privacy">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Personvern
                    </a>
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h2 className="mb-6 text-sm font-semibold text-text uppercase dark:text-white">
                Support
              </h2>
              <ul>
                <li className="mb-4">
                  <Link href="/about/contact">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Kontakt oss
                    </a>
                  </Link>
                </li>
                <li className="mb-4">
                  <Link href="/about/faq">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Spørsmål og svar
                    </a>
                  </Link>
                </li>
                <li className="mb-4">
                  <Link href="/guarantee">
                    <a className="text-text hover:underline dark:text-gray-400">
                     Garanti og forsikring
                    </a>
                  </Link>
                </li>
                <li className="mb-4">
                  <Link href="/about/tutorial">
                    <a className="text-text hover:underline dark:text-gray-400">
                      Slik fungerer Trenger
                    </a>
                  </Link>
                </li>
              </ul>
            </div>
          </div>
      </div>
    </footer>
  )
};