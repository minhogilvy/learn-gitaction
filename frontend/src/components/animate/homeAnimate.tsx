import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { CustomEase } from "gsap/dist/CustomEase";

gsap.registerPlugin(useGSAP, CustomEase);

export default function HomeAminate() {
  const animate = useRef<any[]>([])

  useEffect(() => {
    animate.current.push(gsap.from(".js--circle-lg", {
      scale: 0,
      duration: 0.8,
      ease: "power1.out",
    }))
    animate.current.push(gsap.from(".js--circle-sm", {
      scale: 0,
      duration: 1,
      ease: "power1.out"
    }))
    animate.current.push(
      gsap.fromTo(".js--note", {
        scale: 0.5,
        opacity: 0,
      }, {
        opacity: 1,
        scale: 1.03,
        duration: 0.5,
        ease: "power1.out",
        delay: 0.4,
      }),
      gsap.to(".js--note", {
        scale: 1,
        duration: 1,
        ease: "power1.inOut",
        delay: 0.9,
        yoyo: true,
        repeat: -1
      }))
    animate.current.push(
      gsap.fromTo(".js--teeth", {
        scale: 0.5,
        opacity: 0,
      }, {
        scale: 1.04,
        opacity: 1,
        duration: 0.5,
        ease: "power1.out",
        delay: 0.5,
      }),
      gsap.to(".js--teeth", {
        scale: 1,
        duration: 1,
        ease: "power1.inOut",
        delay: 1,
        yoyo: true,
        repeat: -1
      })
    )
    animate.current.push(gsap.from(".js--bar-1", {
      scaleX: 0.5,
      x: -100,
      opacity: 0,
      duration: 0.6,
      ease: "power1.out",
      delay: 0.4,
    }))
    animate.current.push(gsap.from(".js--bar-2", {
      scaleX: 0,
      x: -50,
      opacity: 0,
      duration: 0.7,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(".js--bar-3", {
      x: -70,
      opacity: 0,
      duration: 0.8,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(".js--bar-4", {
      scaleX: 0,
      x: -100,
      opacity: 0,
      duration: 0.7,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(".js--star-1", {
      scale: 0,
    }))
    animate.current.push(gsap.from(".js--star-2", {
      scale: 0,
      duration: 0.8,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.103,0.068 0.224,0.277 0.313,0.431 0.306,0.41 0.372,0.569 0.444,0.746 0.447,0.734 0.5,0.891 0.562,1.077 0.567,1.092 0.628,1.239 0.671,1.344 0.673,1.383 0.72,1.457 0.786,1.56 0.811,1.477 0.859,1.374 0.952,1.169 1,1 1,1 "),
      delay: 0.8
    }))
    animate.current.push(gsap.fromTo(".js--rounded-1", {
      strokeDashoffset: 100
    }, {
      duration: 2,
      ease: "power1.out",
      strokeDashoffset: 100 / 3 * 2,
      delay: 0.8,
    }))
    animate.current.push(gsap.fromTo(".js--rounded-2", {
      strokeDashoffset: -100 / 3 * 2
    }, {
      duration: 1,
      ease: "power1.out",
      strokeDashoffset: 0,
      delay: 1,
    }))
    animate.current.push(gsap.from(".js--circle-1", {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.8
    }))
    animate.current.push(gsap.from(".js--circle-2", {
      scale: 0,
      duration: 1.2,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 1
    }))
    animate.current.push(gsap.from(".js--circle-3", {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.5
    }))
  }, [])

  return (
    <>
      <div className="relative w-[326px] sm:w-[447px] aspect-[326/269] pointer-events-none">
        <div className="absolute w-[calc(192/326*100%)] top-[calc(129/269*100%)] left-[calc(163/326*100%)] aspect-square translate-x-[-50%] translate-y-[-50%] rounded-full pointer-events-auto js--circle-lg" style={{ backgroundColor: `rgba(223, 77, 86, 0.80)`, boxShadow: `0px 7.2px 21.6px 0px rgba(255, 255, 255, 0.15) inset` }}></div>
        <div className="absolute w-[calc(132/326*100%)] top-[calc(129/269*100%)] left-[calc(163/326*100%)] aspect-square translate-x-[-50%] translate-y-[-50%] rounded-full js--circle-sm" style={{ backgroundColor: `rgba(237, 153, 158, 0.70)`, boxShadow: `0px 7.2px 21.6px 0px rgba(255, 255, 255, 0.60) inset` }}></div>
        <img src="/images/animate/note.svg" alt="" className="absolute w-[27%] left-[59%] top-[36%] aspect-[88/119] translate-x-[-50%] translate-y-[-50%] origin-bottom js--note" />
        <img src="/images/animate/teeth.svg" alt="" className="absolute w-[27%] left-[40%] top-[50%] aspect-[89/94] translate-x-[-50%] translate-y-[-50%] origin-bottom js--teeth" />
        <div className="absolute w-[calc(48/326*100%)] left-[5.35%] top-[52%] h-[3px] bg-red-25 rounded-full opacity-50 js--bar-1"></div>
        <div className="absolute w-[calc(31/326*100%)] left-[1%] top-[calc(160/269*100%)] h-[3px] bg-red-25 rounded-full opacity-50 js--bar-2"></div>
        <div className="absolute w-[calc(23/326*100%)] left-[calc(285/326*100%)] top-[calc(141/269*100%)] h-[3px] bg-red-50 rounded-full opacity-50 js--bar-3"></div>
        <div className="absolute w-[calc(23/326*100%)] left-[calc(302/326*100%)] top-[calc(128/269*100%)] h-[3px] bg-red-25 rounded-full opacity-50 js--bar-4"></div>
        <div className="absolute w-[calc(14/326*100%)] aspect-square left-[calc(58/326*100%)] top-[calc(49/269*100%)] bg-[url(/images/animate/star.svg)] bg-contain opacity-50 js--star-1"></div>
        <div className="absolute w-[calc(10/326*100%)] aspect-square left-[calc(272/326*100%)] top-[calc(190/269*100%)] bg-[url(/images/animate/star.svg)] bg-contain opacity-50 js--star-2"></div>
        <svg className="absolute w-[calc(6/326*100%)] aspect-square left-[calc(293/326*100%)] top-[calc(79/269*100%)]  opacity-50" xmlns="http://www.w3.org/2000/svg" width="10" height="9" viewBox="0 0 10 9" fill="none">
          <path className="js--rounded-1" d="M5.07168 7.45292C6.6732 7.45292 7.97149 6.15464 7.97149 4.55312C7.97149 2.95161 6.6732 1.65332 5.07168 1.65332C3.47017 1.65332 2.17188 2.95161 2.17188 4.55312C2.17188 6.15464 3.47017 7.45292 5.07168 7.45292Z" stroke="#F8D9DB" stroke-width="2.53985" stroke-miterlimit="10" strokeDasharray={"100"} />
        </svg>
        <svg className="absolute w-[calc(10/326*100%)] aspect-square left-[calc(34/326*100%)] top-[calc(190/269*100%)]  opacity-50" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path className="js--rounded-2" d="M6.91847 12.6348C9.85761 12.6348 12.2403 10.2521 12.2403 7.31301C12.2403 4.37387 9.85761 1.99121 6.91847 1.99121C3.97933 1.99121 1.59668 4.37387 1.59668 7.31301C1.59668 10.2521 3.97933 12.6348 6.91847 12.6348Z" stroke="#F8D9DB" stroke-width="2.12872" stroke-miterlimit="10" strokeDasharray={"100"} />
        </svg>

        <div className="absolute w-[calc(5/326*100%)] aspect-square left-[calc(11/326*100%)] top-[calc(77/269*100%)] bg-red-25 rounded-full opacity-50 js--circle-1"></div>
        <div className="absolute w-[calc(6/326*100%)] aspect-square left-[calc(278/326*100%)] top-[calc(109/269*100%)] bg-red-25 rounded-full js--circle-2 opacity-50"></div>
        <div className="absolute w-[calc(9/326*100%)] aspect-square left-[calc(71/326*100%)] top-[calc(212/269*100%)] bg-red-25 rounded-full js--circle-3 opacity-50"></div>
      </div>
    </>
  )
}