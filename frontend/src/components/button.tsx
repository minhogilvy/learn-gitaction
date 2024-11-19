export default function Button({
  children,
  className,
  variant,
  loading,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "white", loading?: boolean }) {
  return (
    <button className={`appearance-none w-[280px] relative pt-1 ${className}`} {...props}>
      <div
        className={`appearance-none h-[46px] px-4 rounded-full flex justify-center items-center gap-3 text-[20px] font-bold capitalize text-center ${variant === "secondary" ? "bg-default text-white" : variant === "white" ? "bg-white text-red-100" : "bg-red-100 text-white"}`}
      >
        {loading && (<img src="/images/icon-loading.svg" alt="" className="block w-6 animate-spin" />)}
        {children}
      </div>
      <svg width="24" height="50" viewBox="0 0 24 50" fill="none" className={`block absolute right-0 bottom-0 w-[24px] h-[50px] ${variant === "secondary" ? "text-default" : variant === "white" ? "text-white" : "text-red-100"}`}>
        <path
          d="M0.599121 50C13.5216 50 24.0001 39.5216 24.0001 26.5991C24.0001 24.077 23.5952 21.6477 22.856 19.3708C22.8412 19.2705 22.804 19.1553 22.7409 19.0142C22.7297 18.9882 22.7186 18.9585 22.7074 18.9325C22.5997 18.6242 22.4883 18.3196 22.3694 18.0187C21.7083 16.0204 21.0991 13.0451 20.9616 12.3616C18.8779 1.56749 20.241 0 20.241 0C15.8543 3.86301 3.61153 3.98514 2.6792 4C1.74688 4.01486 1.32344 4 0.599121 4"
          fill="currentColor" />
      </svg>
    </button>
  );
}