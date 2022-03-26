export default function Button({className, onClick, type, children}) {
  return(
    <button onClick={onClick || null} type={type} className={`inline-block px-6 py-3 rounded-lg dark:bg-blue-200 dark:text-blue-800 ${className}`}>
      {children}
    </button>
  )
}