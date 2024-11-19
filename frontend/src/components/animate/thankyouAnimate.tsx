import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { CustomEase } from "gsap/dist/CustomEase";

gsap.registerPlugin(useGSAP, CustomEase);

export default function ThankyouAminate({ className }: {className: string}) {
  const animate = useRef<any[]>([])
  const container = useRef<HTMLDivElement>(null)

  useEffect(() => {
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-lg")!, {
      scale: 0,
      duration: 0.8,
      ease: "power1.out",
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-sm")!, {
      scale: 0,
      duration: 1,
      ease: "power1.out"
    }))
    animate.current.push(
      gsap.fromTo(container.current?.querySelector(".js--note")!, {
        scale: 0.5,
        opacity: 0,
      }, {
        opacity: 1,
        scale: 1.03,
        duration: 0.5,
        ease: "power1.out",
        delay: 0.4,
      }),
      gsap.to(container.current?.querySelector(".js--note")!, {
        scale: 1,
        duration: 1,
        ease: "power1.inOut",
        delay: 0.9,
        yoyo: true,
        repeat: -1
      }))
    animate.current.push(
      gsap.fromTo(container.current?.querySelector(".js--teeth")!, {
        scale: 0.5,
        opacity: 0,
      }, {
        scale: 1.04,
        opacity: 1,
        duration: 0.5,
        ease: "power1.out",
        delay: 0.5,
      }),
      gsap.to(container.current?.querySelector(".js--teeth")!, {
        scale: 1,
        duration: 1,
        ease: "power1.inOut",
        delay: 1,
        yoyo: true,
        repeat: -1
      })
    )
    animate.current.push(
      gsap.fromTo(container.current?.querySelector(".js--teeth-shadow")!, {
        scale: 0.5,
        opacity: 0,
      }, {
        scale: 1.04,
        opacity: 1,
        duration: 0.5,
        ease: "power1.out",
        delay: 0.5,
      }),
    )
    animate.current.push(gsap.from(container.current?.querySelector(".js--bar-1")!, {
      scaleX: 0,
      x: -100,
      opacity: 0,
      duration: 0.6,
      ease: "power1.out",
      delay: 0.4,
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--bar-2")!, {
      scaleX: 0,
      x: -50,
      opacity: 0,
      duration: 0.7,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--bar-3")!, {
      x: -70,
      opacity: 0,
      duration: 0.8,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--bar-4")!, {
      scaleX: 0,
      x: -100,
      opacity: 0,
      duration: 0.7,
      ease: "power1.out"
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--star-1")!, {
      scale: 0,
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--star-2")!, {
      scale: 0,
      duration: 0.8,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.103,0.068 0.224,0.277 0.313,0.431 0.306,0.41 0.372,0.569 0.444,0.746 0.447,0.734 0.5,0.891 0.562,1.077 0.567,1.092 0.628,1.239 0.671,1.344 0.673,1.383 0.72,1.457 0.786,1.56 0.811,1.477 0.859,1.374 0.952,1.169 1,1 1,1 "),
      delay: 0.8
    }))
    animate.current.push(gsap.fromTo(container.current?.querySelector(".js--rounded-1")!, {
      strokeDashoffset: 100
    }, {
      duration: 2,
      ease: "power1.out",
      strokeDashoffset: 100 / 3 * 2,
      delay: 0.8,
    }))
    animate.current.push(gsap.fromTo(container.current?.querySelector(".js--rounded-2")!, {
      strokeDashoffset: -100 / 3 * 2
    }, {
      duration: 1,
      ease: "power1.out",
      strokeDashoffset: 0,
      delay: 1,
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-1")!, {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.4
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-2")!, {
      scale: 0,
      duration: 1.2,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 1
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-3")!, {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.5
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-4")!, {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.8
    }))
    animate.current.push(gsap.from(container.current?.querySelector(".js--circle-5")!, {
      scale: 0,
      duration: 1,
      ease: CustomEase.create("custom", "M0,0 C0,0 0.031,0.289 0.077,0.601 0.132,0.984 0.106,0.857 0.163,1.188 0.218,1.515 0.206,1.452 0.252,1.68 0.303,1.933 0.294,1.87 0.348,2.054 0.382,2.172 0.575,2.153 0.599,2.08 0.762,1.572 0.77,1.594 0.886,1.222 0.944,1.034 1,1 1,1 "),
      delay: 0.6
    }))
    animate.current.push(
      gsap.fromTo(container.current?.querySelector(".js--check-circle")!, {
        scale: 0,
      }, {
        scale: 1.01,
        duration: 1,
        ease: "power1.inOut",
        delay: 0.7
      }),
      gsap.to(container.current?.querySelector(".js--check-circle")!, {
        scale: 0.9,
        duration: 1,
        ease: "power1.inOut",
        delay: 1.7,
        yoyo: true,
        repeat: -1
      }))
    animate.current.push(
      gsap.to(container.current?.querySelector(".js--check-container")!, {
        scale: 1.4,
        duration: 0.6,
        ease: 'power1.out',
        delay: 1.5,
      }),
      gsap.to(container.current?.querySelector(".js--check-container")!, {
        scale: 1,
        duration: 0.6,
        ease: 'power1.inOut',
        delay: 2.1,
      })
    )
    animate.current.push(
      gsap.fromTo(container.current?.querySelector(".js--check")!, {
        width: "0%",
      }, {
        width: "100%",
        duration: 1,
        ease: "power1.inOut",
        delay: 0.8,
      })
    )
  }, [])
  return (
    <>
      <div ref={container} className={`relative w-[230px] sm:w-[400px] aspect-[230/185] ${className}`}>
        <img src="/images/animate/ty-bg.svg" alt="" className="absolute w-[calc(134/230*100%)] aspect-square left-[calc(47/230*100%)] top-[calc(42/185*100%)] object-contain js--bg" />
        <img src="/images/animate/ty-note.svg" alt="" className="absolute w-[calc(75/230*100%)] aspect-[75/102] left-[calc(97/230*100%)] top-[calc(38/185*100%)] object-contain js--note" />
        <img src="/images/animate/ty-teeth.svg" alt="" className="absolute w-[calc(76/230*100%)] aspect-[76/81] left-[calc(52/230*100%)] top-[calc(73/185*100%)] object-contain js--teeth" />
        <img src="/images/animate/ty-teeth-shadow.svg" alt="" className="absolute w-[calc(61/230*100%)] aspect-[61/6] top-[calc(156/185*100%)] left-[calc(64/230*100%)] object-contain js--teeth-shadow" />
        <div className="absolute w-[calc(40/230*100%)] left-[calc(12/230*100%)] top-[calc(120/185*100%)] h-[5px] bg-red-50 rounded-full js--bar-1"></div>
        <div className="absolute w-[calc(30/230*100%)] left-[calc(2/230*100%)] top-[calc(134/185*100%)] h-[5px] bg-red-25 rounded-full js--bar-2"></div>
        <div className="absolute w-[calc(20/230*100%)] left-[calc(198/230*100%)] top-[calc(86/185*100%)] h-[5px] bg-red-25 rounded-full js--bar-3"></div>
        <div className="absolute w-[calc(20/230*100%)] left-[calc(190/230*100%)] top-[calc(96/185*100%)] h-[5px] bg-red-50 rounded-full js--bar-4"></div>
        <img src="/images/animate/star.svg" alt="" className="absolute w-[calc(12/230*100%)] aspect-square left-[calc(50/230*100%)] top-[calc(40/185*100%)] object-contain js--star-1" />
        <img src="/images/animate/star.svg" alt="" className="absolute w-[calc(10/230*100%)] aspect-square left-[calc(175/230*100%)] top-[calc(148/185*100%)] object-contain js--star-2" />
        <svg className="absolute w-[calc(8/230*100%)] aspect-square left-[calc(194/230*100%)] top-[calc(44/185*100%)]" xmlns="http://www.w3.org/2000/svg" width="10" height="9" viewBox="0 0 10 9" fill="none">
          <path className="js--rounded-1" d="M5.07168 7.45292C6.6732 7.45292 7.97149 6.15464 7.97149 4.55312C7.97149 2.95161 6.6732 1.65332 5.07168 1.65332C3.47017 1.65332 2.17188 2.95161 2.17188 4.55312C2.17188 6.15464 3.47017 7.45292 5.07168 7.45292Z" stroke="#F8D9DB" stroke-width="2.53985" stroke-miterlimit="10" strokeDasharray={"100"} />
        </svg>
        <svg className="absolute w-[calc(14/230*100%)] aspect-square left-[calc(26/230*100%)] top-[calc(158/185*100%)]" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path className="js--rounded-2" d="M6.91847 12.6348C9.85761 12.6348 12.2403 10.2521 12.2403 7.31301C12.2403 4.37387 9.85761 1.99121 6.91847 1.99121C3.97933 1.99121 1.59668 4.37387 1.59668 7.31301C1.59668 10.2521 3.97933 12.6348 6.91847 12.6348Z" stroke="#F8D9DB" stroke-width="2.12872" stroke-miterlimit="10" strokeDasharray={"100"} />
        </svg>
        <div className="absolute w-[calc(4/230*100%)] aspect-square left-[calc(12/230*100%)] top-[calc(65/185*100%)] bg-red-25 rounded-full js--circle-1"></div>
        <div className="absolute w-[calc(7/230*100%)] aspect-square left-[calc(32/230*100%)] top-[calc(86/185*100%)] bg-red-25 rounded-full js--circle-2"></div>
        <div className="absolute w-[calc(5/230*100%)] aspect-square left-[calc(64/230*100%)] top-[calc(180/185*100%)] bg-red-25 rounded-full js--circle-3"></div>
        <div className="absolute w-[calc(4/230*100%)] aspect-square left-[calc(126/230*100%)] top-[calc(4/185*100%)] bg-red-25 rounded-full js--circle-4"></div>
        <div className="absolute w-[calc(5/230*100%)] aspect-square left-[calc(188/230*100%)] top-[calc(73/185*100%)] bg-red-25 rounded-full js--circle-5"></div>
        <div className="absolute w-[calc(49/230*100%)] aspect-square left-[calc(117/230*100%)] top-[calc(128/185*100%)] bg-red-100 rounded-full js--check-circle flex justify-center items-center">
          <div className="w-[calc(37/49*100%)] aspect-[37/28] js--check-container relative">
            <img src="/images/animate/ty-check.svg" className="absolute h-full left-0 top-0 object-cover object-left js--check" alt="" />
          </div>
        </div>
      </div>
    </>
  )
}