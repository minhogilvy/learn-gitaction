import "@/assets/css/global.css"
import localFont from 'next/font/local'

const colgateReady = localFont({
  src: [
    {
      path: '../../public/fonts/ColgateReady-Light.otf',
      weight: '300',
    },
    {
      path: '../../public/fonts/ColgateReady-LightItalic.otf',
      weight: '300',
      style: 'italic'
    },
    {
      path: '../../public/fonts/ColgateReady-Regular.otf',
      weight: '400',
    },
    {
      path: '../../public/fonts/ColgateReady-Bold.otf',
      weight: '700',
    },
    {
      path: '../../public/fonts/ColgateReady-BoldItalic.otf',
      weight: '700',
      style: 'italic'
    },
    {
      path: '../../public/fonts/ColgateReady-Heavy.otf',
      weight: '900',
    },
    {
      path: '../../public/fonts/ColgateReady-HeavyItalic.otf',
      weight: '900',
      style: 'italic'
    },
  ],
  variable: '--font-colgate-ready',
})
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <main className={`flex flex-col w-full h-dvh overflow-hidden text-default font-colgate ${colgateReady.className} ${colgateReady.variable}`}>{children}</main>
    </>
  )
}