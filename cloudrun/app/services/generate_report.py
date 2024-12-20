import asyncio
from loguru import logger
from app.services.firebase import FirebaseService
from app.utils.helpers import Helpers


utils = Helpers()
firebase = FirebaseService()
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Colgate</title>
  <link rel="stylesheet" href="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/styles/index.css">
</head>

<body>
  <div class="onepage-printer">
    <div class="outer">
      <div class="main-container">
        <header>
          <img class="logo" src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/logo.png" alt="Colgate Logo" />
          <p class="desc">Welcome to your</p>
          <h1 class="head">Oral Health Screening Report</h1>
          <div class="sponsor-group">
            <div class="line"></div>
            <div class="text">In association with:</div>
            <div class="logos">
              <div>
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/sponsor-1.png" alt="Sponsor Logo">
              </div>
              <div>
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/sponsor-2.png" alt="Sponsor Logo">
              </div>
            </div>
          </div>
        </header>
        <section class="section section-1">
          <label class="label">
            <span>Name</span>
            <span>{name}</span>
          </label>
          <div class="row">
            <label class="label">
              <span>Gender</span>
              <span>{gender}</span>
            </label>
            <label class="label">
              <span>Age</span>
              <span>{age}</span>
            </label>
          </div>
        </section>
        <section class="section section-2">
          <div class="row">
            <h3 class="title">
              Habits questions:
              <span class="small">answered: {answered_date}</span>
            </h3>
          </div>
          <div class="row row-border">
            <div class="question">Teeth or gums hurt?</div>
            <div class="answer">{answer_for_question_1}</div>
          </div>
          <div class="row row-border">
            <div class="question">Bleeding gums?</div>
            <div class="answer">{answer_for_question_2}</div>
          </div>
          <div class="row row-border">
            <div class="question">Moving or loose teeth?</div>
            <div class="answer">{answer_for_question_3}</div>
          </div>
          <div class="row row-border">
            <div class="question">How often: teeth brush?</div>
            <div class="answer">{answer_for_question_4}</div>
          </div>
          <div class="row row-border">
            <div class="question">How often: Sugar intake?</div>
            <div class="answer">{answer_for_question_5}</div>
          </div>
          <div class="row">
            <div class="question">Smoker?</div>
            <div class="answer">{answer_for_question_6}</div>
          </div>
        </section>
        <section class="section section-3">
          <div class="block">
            <svg xmlns="http://www.w3.org/2000/svg" width="61" height="61" viewBox="0 0 61 61" fill="none">
              <g clip-path="url(#clip0_364_676)">
                <path
                  d="M30.5 5.71875C25.5987 5.71875 20.8075 7.17214 16.7323 9.89514C12.657 12.6181 9.48076 16.4884 7.60512 21.0166C5.72949 25.5448 5.23874 30.5275 6.19493 35.3346C7.15112 40.1417 9.5113 44.5573 12.977 48.023C16.4427 51.4887 20.8583 53.8489 25.6654 54.8051C30.4725 55.7613 35.4552 55.2705 39.9834 53.3949C44.5116 51.5193 48.3819 48.343 51.1049 44.2677C53.8279 40.1925 55.2813 35.4013 55.2813 30.5C55.2738 23.9299 52.6606 17.631 48.0148 12.9852C43.369 8.33942 37.0701 5.72617 30.5 5.71875ZM28.5938 19.0625C28.5938 18.5569 28.7946 18.0721 29.1521 17.7146C29.5096 17.3571 29.9944 17.1562 30.5 17.1562C31.0056 17.1562 31.4904 17.3571 31.8479 17.7146C32.2054 18.0721 32.4063 18.5569 32.4063 19.0625V32.4062C32.4063 32.9118 32.2054 33.3967 31.8479 33.7542C31.4904 34.1117 31.0056 34.3125 30.5 34.3125C29.9944 34.3125 29.5096 34.1117 29.1521 33.7542C28.7946 33.3967 28.5938 32.9118 28.5938 32.4062V19.0625ZM30.5 43.8438C29.9345 43.8438 29.3816 43.676 28.9114 43.3619C28.4412 43.0477 28.0747 42.6011 27.8583 42.0786C27.6419 41.5561 27.5852 40.9812 27.6956 40.4265C27.8059 39.8719 28.0782 39.3624 28.4781 38.9625C28.878 38.5626 29.3875 38.2903 29.9422 38.1799C30.4968 38.0696 31.0718 38.1262 31.5942 38.3427C32.1167 38.5591 32.5633 38.9256 32.8775 39.3958C33.1917 39.866 33.3594 40.4188 33.3594 40.9844C33.3594 41.7427 33.0581 42.47 32.5219 43.0063C31.9857 43.5425 31.2584 43.8438 30.5 43.8438Z"
                  fill="#D2010D" />
              </g>
              <defs>
                <clipPath id="clip0_364_676">
                  <rect width="61" height="61" fill="white" />
                </clipPath>
              </defs>
            </svg>
            <h3 class="title">Disclaimer</h3>
            <p class="desc">This is a preliminary analysis by Al software and is not conclusive.</p>
            <p class="note">Please see your dentist for further assessment and possible treatment. This is not a trauma
              assessment tool. Contact healthcare provider before taking any steps.</p>
          </div>
        </section>
        <section class="section section-4">
          <div class="block block-1">
            <h3 class="title">Your score</h3>
            <p class="desc">Check your oral care report, based on the information you provided:</p>
          </div>
          <div class="block block-2">
            <h3 class="title">Potential risks</h3>
            <p class="desc">Based on the questions and the photos there's a potential occurrence of the following risks:
            </p>
          </div>
          <div class="block block-3">
            <div class="line-top">
              <svg xmlns="http://www.w3.org/2000/svg" width="322" height="22" viewBox="0 0 322 22" fill="none">
                <path
                  d="M321 20.9377V17C321 11.3995 321 8.59921 319.91 6.46009C318.951 4.57847 317.422 3.04867 315.54 2.08993C313.401 1 310.601 1 305 1H17C11.3995 1 8.59921 1 6.46009 2.08993C4.57847 3.04867 3.04867 4.57847 2.08993 6.46009C1 8.59921 1 11.3995 1 17V20.9377"
                  stroke="#D2010D" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <div class="line-bottom">
              <svg xmlns="http://www.w3.org/2000/svg" width="322" height="22" viewBox="0 0 322 22" fill="none">
                <path
                  d="M321 1.00005V4.93774C321 10.5383 321 13.3385 319.91 15.4776C318.951 17.3593 317.422 18.8891 315.54 19.8478C313.401 20.9377 310.601 20.9377 305 20.9377H17C11.3995 20.9377 8.59921 20.9377 6.46009 19.8478C4.57847 18.8891 3.04867 17.3593 2.08993 15.4776C1 13.3385 1 10.5383 1 4.93774V1.00005"
                  stroke="#D2010D" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <div class="note">Remember:</div>
            <p class="small-note">The comorbidities found in this report are the most common in oral care.</p>
            <p class="small-note"> Therefore, the result will not take into account all existing comorbidities. </p>
          </div>
        </section>
        <!--  -->
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">1</div>
            <div class="circle"></div>
            <div class="text">Tooth Caries</div>
            <div class="{caries_style}">{caries}</div>
            <p class="desc">Occurs when bacteria produce acids from sugars, leading to color changes like white, yellow, brown, or black spots on the tooth surface, especially in grooves and fissures.</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">2</div>
            <div class="circle"></div>
            <div class="text">Gingivitis</div>
            <div class="{gingivitis_style}">{gingivitis}</div>
            <p class="desc">Occurs when bacteria produce acids from sugars, leading to color changes like white, yellow, brown, or black spots on the tooth surface, especially in grooves and fissures.</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">3</div>
            <div class="circle"></div>
            <div class="text">Calculus</div>
            <div class="{calculus_style}">{calculus}</div>
            <p class="desc">Occurs when bacteria produce acids from sugars, leading to color changes like white, yellow, brown, or black spots on the tooth surface, especially in grooves and fissures.</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">4</div>
            <div class="circle"></div>
            <div class="text">Mouth Ulcers</div>
            <div class="{mouthUlcers_style}">{mouthUlcers}</div>
            <p class="desc">Occurs when bacteria produce acids from sugars, leading to color changes like white, yellow, brown, or black spots on the tooth surface, especially in grooves and fissures.</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">5</div>
            <div class="circle"></div>
            <div class="text">Discoloration</div>
            <div class="{discoloration_style}">{discoloration}</div>
            <p class="desc">Dental plaque is a sticky biofilm of bacteria that develops on mouth surfaces shortly after brushing.
            If not removed, it can cause cavities (dental caries) and gum issues like gingivitis.t</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-5">
          <div class="block block-1">
            <div class="number">6</div>
            <div class="circle"></div>
            <div class="text">Dental Plaque</div>
            <div class="tag red">Very likely</div>
            <p class="desc">Tooth decay is the destruction of tooth tissue caused by bacteria that produce acids from sugars.
            This process results in color changes such as white, yellow, brown, or black spots on the surface of the teeth, particularly in the grooves and fissures.</p>
          </div>
          <div class="block block-2">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#D6D6D6" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Main symptoms:</div>
              <ul>
                <li>Discomfort and increased sensitivity</li>
                <li>Bad breath</li>
                <li>Pain when exposed to hot, cold, or sweet stimuli</li>
                <li>Intense spontaneous pain as the decay reaches deeper layers of the tooth</li>
              </ul>
            </div>
          </div>
          <div class="block block-3">
            <div class="decor">
              <svg xmlns="http://www.w3.org/2000/svg" width="328" height="66" viewBox="0 0 328 66" fill="none">
                <path d="M0 25.4082C99.7327 76.5092 250.735 61.6944 328 0V66H0V25.4082Z" fill="#F3F3F3" />
              </svg>
            </div>
            <div class="content">
              <div class="headline">Recommendations?</div>
              <p class="desc">This is what you can do:</p>
              <div class="list">
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-1.png" alt="item">
                  </div>
                  <div class="text">Maintain proper oral hygiene by brushing teeth at least three times a day.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-2.png" alt="item">
                  </div>
                  <div class="text">Use dental floss regularly to clean between teeth and prevent plaque buildup.</div>
                </div>
                <div class="item">
                  <div class="icon">
                    <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-5-icon-3.png" alt="item">
                  </div>
                  <div class="text">Make sure your diet is low in sugary foods and drinks to minimize future risk.</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <!--  -->
        <section class="section section-6">
          <div class="thumb">
            <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-6-thumb.png" alt="Thumb">
          </div>
          <div class="headline">
            <h2 class="head">
              <span>Wish to help</span>
              <span class="bold">someone else?</span>
            </h2>
            <p class="desc">Do you know someone else who would also like to do the oral care report? Share it!</p>
          </div>
          <ul class="list">
            <li>
              <a href="https://web.whatsapp.com/" target="_blank">
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/button-whatsapp.png" alt="button">
              </a>
            </li>
            <li>
              <a href="https://www.facebook.com/" target="_blank">
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/button-facebook.png" alt="button">
              </a>
            </li>
            <li>
              <a href="https://www.instagram.com/" target="_blank">
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/button-instagram.png" alt="button">
              </a>
            </li>
          </ul>
        </section>
        <section class="section section-7">
          <div class="content">
            <div>
              <img width="188" src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-7-logo.png" alt="Logo" />
            </div>
            <div class="row">
              <p class="note">Brightening Our Communities</p>
              <h3 class="title">One Smile at a Time</h3>
            </div>
            <div>
              <p class="desc">Discover what the <b>Colgate Bright Smiles, Bright Futures®</b> mobile dental van means to
                the communities, children, dentists and volunteers it serves.</p>
            </div>
          </div>
          <div class="images">
            <div class="row">
              <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-7-img-1.png" alt="Image" />
            </div>
            <div class="row">
              <div class="col col-6">
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-7-img-2.png" alt="Image" />
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-7-img-3.png" alt="Image" />
              </div>
              <div class="col col-4">
                <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-7-img-4.png" alt="Image" />
                <div class="block-more">
                  <a href="https://www.youtube.com/" target="_blank">
                    <div class="text">
                      <b>Watch</b><br />
                      the video
                    </div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="46" height="47" viewBox="0 0 46 47" fill="none">
                      <path
                        d="M15.3335 33.4283V13.5716C15.3335 12.0575 17.001 11.1375 18.2852 11.9616L33.8868 21.89C35.0752 22.6375 35.0752 24.3625 33.8868 25.1291L18.2852 35.0383C17.001 35.8625 15.3335 34.9425 15.3335 33.4283Z"
                        fill="#D2010D" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section class="section section-8">
          <div class="thumb">
            <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/section-8-thumb.png" alt="Thumb">
          </div>
          <div class="content">
            <div class="logo-1">
              <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/sponsor-1.png" alt="Logo">
            </div>
            <div class="text">
              <div class="note">National Department of Health:</div>
              <a class="link" target="_blank" href="https://www.health.gov.za/">https://www.health.gov.za/</a>
            </div>
            <div class="text">
              <div class="small-note">Phone:</div>
              <div class="small-note text-black">0800 012 322</div>
            </div>
            <div class="divider"></div>
            <div class="logo-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="198" height="60" viewBox="0 0 198 60" fill="none">
                <g clip-path="url(#clip0_219_231)">
                  <path
                    d="M34.6725 0C31.6784 0 32.9425 4.44966 33.1754 5.91074C33.1754 5.97716 33.4083 15.9723 33.4748 18.2635C33.9406 18.1307 34.3731 18.0311 34.8388 17.9315L35.7371 17.699C35.7703 15.4742 36.0032 5.94395 36.0032 5.87754C36.2028 4.35004 37.7664 0 34.6725 0ZM33.8408 33.8705C34.1735 33.7709 34.5061 33.6381 34.8056 33.5717C35.0384 33.5053 35.238 33.4389 35.4709 33.3725C35.4709 32.7415 35.6705 23.8422 35.7038 22.2483C35.0052 22.4143 34.3065 22.6136 33.6412 22.846C33.6744 24.0415 33.8408 32.9076 33.8408 33.8705ZM35.0052 37.1912C34.9054 37.2244 34.6059 37.3572 34.4063 37.4236C34.2067 37.49 33.9739 37.5897 33.9739 37.6561C33.9739 37.6561 34.1735 47.8837 34.1735 48.0829C34.1735 50.1749 35.238 50.2081 35.238 48.0829C35.238 47.9501 35.4709 37.0252 35.4709 37.0252C35.4709 37.0252 35.1715 37.1248 35.0052 37.1912ZM32.5433 8.70008C31.7449 8.96573 30.9465 9.26459 30.1813 9.66307C29.3496 9.92872 28.1519 9.99513 26.921 11.3234C26.5218 11.7883 26.1559 12.2864 25.7899 12.7845C25.424 13.3158 25.3907 14.1791 25.1245 14.6108C24.7253 15.275 24.8251 15.6734 24.8251 15.6734C24.7586 15.9723 24.5923 16.2711 24.3927 16.5036C23.9934 16.9685 23.3946 17.2009 22.7958 17.1013C23.3613 17.367 24.1265 17.0017 24.1265 17.0017C23.9934 17.367 23.8936 17.7322 23.8271 18.0975C24.4592 16.6696 25.0247 16.1715 25.2244 16.0055C25.4905 16.0719 26.0561 16.0387 27.0874 15.441C28.2517 14.7769 30.015 13.681 30.514 12.9837C31.0463 12.2864 31.7449 11.7219 32.5766 11.423C32.5766 10.4268 32.5433 9.49704 32.5433 8.70008ZM27.6197 13.1165L27.0208 13.2494L27.7527 12.0539L28.5844 12.0871L27.6197 13.1165ZM31.2126 37.5233C31.2126 38.8515 32.1774 39.5488 33.1422 40.1134C33.1422 39.8809 33.1089 37.8553 33.1089 37.8221C33.1422 37.4236 33.5081 37.158 33.8408 37.0252C34.3398 36.7927 34.8721 36.5935 35.4044 36.4274C35.7038 36.3278 35.9367 36.2282 36.2028 36.1618C38.1656 35.5641 40.4279 34.8335 40.4279 32.4427C40.4279 30.0518 38.4983 29.0888 36.3692 28.3583C36.3359 29.122 36.3359 30.2178 36.3026 30.9816C37.2009 31.3137 37.7997 31.7453 37.7997 32.4427C37.7997 33.306 36.9014 33.7709 36.2361 34.0366C35.9699 34.1362 35.5707 34.269 35.4376 34.3022C34.9054 34.4683 34.3731 34.6343 33.8408 34.8335C33.5746 34.9332 33.3085 35.0328 33.0423 35.1656C32.1774 35.6305 31.2126 36.3278 31.2126 37.5233ZM43.9875 14.5112C43.9875 12.0871 42.2243 9.43062 37.9328 8.50084C37.5003 8.43443 37.0678 8.36802 36.6353 8.33481C36.6353 8.70008 36.602 9.53024 36.602 9.53024C36.602 9.79589 36.5688 10.7589 36.5688 10.9581C36.8349 10.9913 37.1343 11.0245 37.4005 11.0577C39.8956 11.6555 40.7938 13.0833 40.7938 14.478C40.7938 16.7692 38.831 17.6326 36.4357 18.2967L35.6373 18.496C34.9054 18.662 34.1402 18.8612 33.4083 19.0605C33.1422 19.1269 32.876 19.1933 32.6099 19.2929C29.9484 20.0899 27.6529 21.3849 27.6529 24.6724C27.6529 27.9598 30.2811 29.1552 32.8427 29.9522C32.8427 29.0224 32.8095 28.0594 32.7762 27.1296C31.6118 26.5983 30.8467 25.901 30.8467 24.7388C30.8467 23.5766 31.5786 22.9124 32.6764 22.4143C32.9093 22.3147 33.1754 22.2151 33.4748 22.1155C34.1069 21.883 34.8388 21.717 35.5707 21.5178L36.3692 21.3185C39.9621 20.4552 44.0208 19.3261 43.9875 14.5112ZM36.0032 41.508C37.2009 42.1057 38.332 42.9691 38.7977 44.563C38.9973 41.9065 37.5003 40.7775 36.0365 39.9805L36.0032 41.508ZM55.964 10.9581C57.2615 12.5188 59.5237 13.4154 60.8544 14.9761C59.8897 10.3936 56.3633 6.64128 52.1715 5.74471C54.2341 7.27221 54.6666 9.39742 55.964 10.9581ZM5.72927 22.5804C8.62359 16.3044 12.9152 17.6326 14.7449 11.6887C13.6803 13.4818 8.98954 14.2456 6.82712 18.9277C7.95823 16.1383 7.39267 11.8879 9.25569 9.56345C3.63338 13.7475 6.02868 20.4552 5.72927 22.5804ZM10.9191 37.5897C11.4514 40.0137 9.92105 43.5668 12.3496 46.9207C9.85451 44.1313 4.53162 43.4008 2.3692 39.1504C5.06391 49.544 12.1167 47.4188 15.2772 49.6768C12.6823 45.9245 14.8115 43.434 10.9191 37.5897ZM10.1207 44.1313C8.55706 38.3202 11.3183 36.2946 9.22242 30.7159C9.02281 33.8705 6.89365 35.398 8.32418 41.1428C5.82908 36.2614 1.96998 34.4351 0.838867 31.1144C0.905403 40.2462 8.25764 41.6076 10.1207 44.1313ZM21.3985 53.8608C19.2361 50.8722 20.6999 49.1787 14.6451 43.7661C15.9426 45.7584 14.6118 48.2489 18.7038 52.1009C14.7116 49.7432 9.15588 50.7394 6.49444 47.5848C11.0854 56.3513 19.1363 52.765 21.3985 53.8608ZM50.8408 52.1009C54.9327 48.2157 53.602 45.7252 54.8995 43.7661C48.8114 49.1787 50.3085 50.8722 48.1128 53.8608C50.4083 52.765 58.4591 56.3513 63.0169 47.5848C60.3887 50.7726 54.8329 49.7432 50.8408 52.1009ZM57.195 46.9207C59.6235 43.5668 58.0932 40.0469 58.5922 37.5897C54.6999 43.434 56.829 45.9245 54.2341 49.6768C57.4278 47.4188 64.4474 49.544 67.1421 39.1504C64.9797 43.4008 59.6901 44.1313 57.195 46.9207ZM47.4807 54.2925C45.3183 53.728 43.0893 53.3627 40.8271 53.2963C38.7645 53.2631 36.7018 53.5952 34.7723 54.3257C32.8427 53.5952 30.7801 53.2631 28.7175 53.2963C26.4553 53.3627 24.2263 53.728 22.0639 54.2925C18.4044 55.2555 15.2439 56.0192 12.4827 54.6246C15.1109 56.949 18.2048 57.8124 22.6627 57.3143C26.3555 56.9158 29.3496 55.0562 32.8427 55.0895H32.9758C30.7801 56.1853 28.8173 57.7128 27.2204 59.5723L28.9171 59.8048C28.9171 59.8048 30.6803 56.2517 34.7723 55.3219C38.8643 56.2517 40.6275 59.8048 40.6275 59.8048L42.3241 59.5723C40.7273 57.7128 38.7645 56.1853 36.5688 55.0895H36.7018C40.195 55.0562 43.1891 56.9158 46.8819 57.3143C51.3398 57.7792 54.4004 56.949 57.0619 54.6246C54.3006 56.0192 51.1402 55.2555 47.4807 54.2925ZM9.5551 24.4067C8.05804 27.2957 5.696 27.9598 5.96215 33.9038C4.69796 28.6239 1.67057 26.6315 1.70384 23.2777C-0.392051 32.1106 5.19698 33.14 6.66078 36.8591C6.4279 31.5461 9.82124 30.4835 9.5551 24.4067ZM11.651 17.5994C11.1187 18.3299 10.7527 18.662 9.35549 19.791C7.2596 21.4513 5.79581 23.809 5.29679 26.4323C5.42986 23.1781 3.43378 18.5292 4.7645 15.1421C-0.392051 22.4143 5.06391 26.7644 5.26352 29.4209C6.56097 24.3403 9.6549 24.3071 11.651 17.5994ZM64.2145 26.4323C63.6822 23.809 62.2517 21.4513 60.1558 19.791C58.7586 18.6288 58.3926 18.3299 57.8603 17.5994C59.8564 24.3071 62.9503 24.3403 64.2811 29.4209C64.4807 26.7976 69.9366 22.4475 64.7801 15.1421C66.1108 18.5292 64.1147 23.1781 64.2145 26.4323ZM68.6059 31.1144C67.4748 34.4683 63.6157 36.2614 61.1206 41.1428C62.5511 35.398 60.422 33.8705 60.2224 30.7159C58.1265 36.2946 60.8877 38.3202 59.3241 44.1313C61.1871 41.6076 68.5394 40.2462 68.6059 31.1144ZM59.9562 24.4067C59.6568 30.4835 63.0834 31.5461 62.8505 36.8591C64.2811 33.1732 69.9034 32.1106 67.8075 23.2777C67.8407 26.6648 64.8133 28.6239 63.5492 33.937C63.8153 27.9266 61.4865 27.2957 59.9562 24.4067ZM13.3809 10.9581C14.6784 9.39742 15.1109 7.27221 17.1735 5.74471C12.9484 6.64128 9.42203 10.3604 8.45725 14.9429C9.78798 13.3822 12.0835 12.4856 13.3809 10.9581ZM54.6333 11.6222C56.4631 17.5994 60.7546 16.2711 63.649 22.514C63.3495 20.4219 65.7449 13.681 60.1225 9.56345C62.0188 11.8547 61.4533 16.1383 62.5511 18.9277C60.3554 14.2456 55.6646 13.4818 54.6333 11.6222ZM39.9954 15.0425C38.8975 14.5776 37.7331 14.2788 36.5688 14.1127V14.8765C37.6666 15.0425 38.7312 15.3414 39.7292 15.7398C39.8623 15.5074 39.9621 15.275 39.9954 15.0425ZM39.1304 7.63748L39.3633 7.43824L38.9308 7.239L37.7664 7.20579L37.467 7.40503L36.8016 7.33862V7.50465C37.2341 7.53786 37.6666 7.57106 37.9993 7.63748L38.5648 7.60427L39.1304 7.63748ZM36.9347 32.4095C36.9347 32.2102 36.6686 32.011 36.3026 31.845H36.2361C36.2361 32.011 36.2028 32.7747 36.2028 33.1732C36.6353 32.9408 36.9347 32.7415 36.9347 32.4095ZM23.5942 17.8318C23.6275 17.699 23.6608 17.533 23.694 17.4002C23.5277 17.4334 23.3946 17.4666 23.2283 17.4334L23.5942 17.8318ZM18.2381 12.4856L20.966 15.2085C17.6725 18.6288 15.8095 23.2113 15.743 27.9598H11.8839C11.9504 22.1487 14.2126 16.6364 18.2381 12.4856ZM16.5747 33.6713L16.3418 33.6381L16.1089 33.4057L15.0111 33.306L15.3437 33.7709L14.3457 33.5717L14.6118 33.3392L14.379 33.1068L13.6471 33.4057L13.3809 33.8705L13.4807 34.9664L14.3124 36.9587L14.7116 37.5897L14.9445 37.6561L14.3124 36.4607L14.1794 35.8629L14.3124 35.7301L14.2126 35.398L14.5786 35.4645L15.1774 36.3278L15.3105 36.3942V35.7633L15.5433 35.8961L15.6099 36.2282L16.2087 36.3942L16.4749 36.195L16.5747 36.2614V36.7263L16.8408 37.0584L17.1735 37.1248L17.9054 38.3202L18.3379 38.453L18.4709 37.8885C19.2361 39.1172 20.1011 40.2794 21.1324 41.3088L18.4044 44.0317C14.3457 39.9473 12.0169 34.4683 11.8839 28.7236H15.743C15.7762 30.3839 16.0756 32.0774 16.5747 33.6713ZM20.3672 28.6903C20.3672 29.0556 20.4005 29.4209 20.467 29.8194L20.0013 29.919L19.9015 30.3839L18.9034 31.6457L18.9367 33.3725L17.9387 33.7045H17.3731C16.8408 32.0774 16.5747 30.4171 16.5081 28.6903H20.3672ZM21.2322 39.5488L22.0972 40.0469L22.2635 40.1798L21.6314 40.8107C21.332 40.5118 21.0658 40.213 20.7997 39.8809L21.2322 39.5488ZM24.7586 18.9941L27.4866 21.717C26.921 22.3479 26.422 23.0453 26.0561 23.809H25.8564L25.4572 23.9086H25.3242L24.9249 24.2739L25.4572 24.2075L25.923 24.1079L25.8232 24.2407L25.424 24.5063H25.2244L24.6255 24.9712L24.06 24.9048L23.2283 26.4655L23.3946 26.7644L22.9289 27.2957L22.8623 27.9598H21.1324C21.1657 24.606 22.4631 21.4181 24.7586 18.9941ZM27.5531 30.251L27.7527 30.1514L28.2517 30.5167L28.0189 30.6827L28.5844 31.048L28.5512 30.6495L28.8506 30.1514L29.1833 30.4835L29.5159 30.9484L28.9171 31.1144L29.1833 31.6457L29.5825 31.4133L29.5159 31.2472L29.8153 31.048L29.9817 30.2178C30.2146 30.7159 30.514 31.1808 30.8799 31.5793L28.1519 34.3022C26.8212 32.9076 25.9895 31.1144 25.7566 29.1884L26.3222 29.7862H26.8545L27.5531 30.251ZM23.6275 27.3621L23.694 26.5983L24.1598 26.3327L24.9915 26.4655L25.1245 26.5983C25.058 27.03 25.0247 27.4949 24.9915 27.9266H24.06L23.6275 27.3621ZM22.3633 30.0186L21.9974 30.5831H21.3653L21.332 30.5499C21.2322 29.9522 21.1657 29.3213 21.1324 28.7236H22.2968L22.0306 29.6533L22.3633 30.0186ZM24.9249 37.5233C24.6588 37.2244 24.3594 36.9255 24.1265 36.6267L24.2596 35.6637L23.8604 34.7339L23.7606 33.2728L23.2948 32.3763L23.3946 31.8118L22.8291 30.7491L22.3633 30.5167L22.5629 29.9522L22.3633 29.5205L22.5629 29.0224H23.0952L23.2948 28.7236H24.193L24.3261 28.9892L24.1265 29.8858L24.0267 30.0518L24.3594 30.7824L24.1265 30.9152L23.9602 30.7159L23.8936 30.7824L24.06 31.214L24.3261 31.7121H24.4592L24.5257 31.2472L24.3927 31.0812V30.7824L24.3594 30.1514L24.559 29.0224L24.3594 28.7236H24.9915C25.1245 31.0148 26.0561 33.1732 27.6529 34.8335L24.9249 37.5233ZM48.146 41.2424C51.4396 37.8553 53.3359 33.3725 53.4357 28.6903H57.2948C57.1617 34.4019 54.8662 39.8809 50.8408 43.9653L48.146 41.2424ZM47.0815 40.1798L47.3809 39.8477L47.0815 38.3534L46.8819 38.287L47.0149 38.0214L46.3828 37.8221L46.2498 38.3534L46.1832 39.0175L46.0502 39.1504L44.8858 37.9881C47.3143 35.4645 48.7116 32.177 48.8447 28.6903H52.7038C52.5707 33.2064 50.7742 37.49 47.6138 40.7111L47.0815 40.1798ZM43.6881 43.7993L44.0541 43.0355L43.921 42.7035L44.4533 42.2386V41.9729L43.9875 41.6741L44.3535 40.9103L44.919 40.1798L44.3535 39.5821H43.921L43.6549 39.1504C43.8877 38.9511 44.1206 38.7519 44.3202 38.5527L47.0482 41.2756C46.0502 42.2386 44.919 43.1019 43.6881 43.7993ZM43.1558 36.2946L42.7899 35.9293L43.056 35.5641L43.422 34.8335L43.2889 34.6343L43.5218 34.103L43.4885 33.6049L43.3554 33.1068L43.0228 33.0072L42.8897 33.2728L42.6901 33.2064C42.9895 32.7747 43.2556 32.2766 43.4885 31.8118L43.8212 31.6789L44.0208 31.4133L44.1206 31.5129L44.3535 31.2472L44.1539 31.0148L44.3202 30.9816L44.6196 31.1144H45.2185L45.5844 30.9152L46.5159 30.6495L46.3496 30.3507L46.283 29.9854L46.7821 30.2178L46.9817 30.1182L46.8819 29.7197L46.2498 29.9522L45.5844 29.8194L45.0521 28.7568H48.013C47.8799 32.0442 46.5492 35.1656 44.2869 37.5233L43.8877 37.1248L44.0541 36.5935L43.7547 35.398L43.1558 36.2946ZM41.7586 21.8166L44.4866 19.0937C45.1187 19.791 45.6842 20.5548 46.1832 21.3517L45.8506 21.4513L45.8838 22.0491L46.8819 22.68C47.148 23.2445 47.3476 23.809 47.514 24.4067L47.3476 24.6724L46.9817 24.938L46.8819 25.5025L46.6157 25.6354L46.4161 25.901L46.2165 25.8014H45.8506L46.0502 25.5025L46.2165 24.7388L46.4826 24.5728L45.7507 23.8754L45.2185 24.0747L45.0854 24.606L44.7527 24.9712L44.3868 24.6724L44.2537 24.3403L44.4533 24.2075L44.5531 24.4067L44.7194 24.3403L44.6529 24.0082H44.42V24.1411L44.2537 24.1743L43.422 23.1781L43.1226 22.9456L43.2224 22.846L43.4885 22.7464L43.2224 22.6468C43.2224 22.6468 42.923 22.7132 42.8897 22.7132L43.056 22.9456H42.6235C42.3574 22.514 42.0913 22.1487 41.7586 21.8166ZM42.1911 36.6599L41.3594 36.4274L41.0932 36.5271L40.6275 36.1618L40.195 35.9958C40.4279 35.8297 40.6275 35.6637 40.8271 35.4977L41.5257 35.9958L42.058 36.2614L42.3241 36.5271L42.1911 36.6599ZM40.7273 23.8754L41.0599 23.809V23.7426L40.7273 23.5101L40.8271 22.7796L41.2263 22.3479C41.4924 22.6468 41.7253 22.9456 41.9582 23.2777L41.8251 23.7094L41.4592 23.4437L41.1598 23.5101L41.2928 23.7758H41.4259L41.2596 24.1743L41.1598 24.0082L40.7273 23.8754ZM45.3515 26.5319L46.0502 26.1667L46.7488 26.067L46.9151 25.735L47.3143 25.5025L47.4807 25.1705L47.6138 24.606C47.6803 24.8052 47.7136 25.0044 47.7801 25.2037L47.4142 26.2995V26.6648L47.8799 25.901C47.9797 26.5651 48.0462 27.2625 48.0795 27.9266H44.6862L44.6196 27.6277L45.0188 27.3289L45.0854 27.1296L45.2517 26.9968L45.7175 26.9304L45.7507 26.7312L45.3515 26.5319ZM46.1167 17.4998L47.0482 17.533L47.2811 17.7986L47.1813 18.1971L48.4787 18.9941L48.7449 18.9609L50.375 20.8536L51.0404 20.6212C52.1049 22.9124 52.6705 25.4361 52.7038 27.9598H48.8447C48.8447 26.9636 48.7116 26.0006 48.4787 25.0376L48.6451 24.8052L48.8779 23.5766L48.7116 22.2815L48.2458 20.7872L47.1813 19.2265L47.4474 19.3593L47.5805 19.2265L46.7155 18.6288L46.649 18.828L47.514 20.0567L48.013 21.0529L48.3457 22.0491L48.4455 22.7132L48.6118 23.8422L48.2791 23.8754C48.2791 23.8754 47.9132 23.1781 47.7801 22.8792L47.9464 22.6136L47.6138 22.1487V21.717L47.3809 21.4181L47.0815 21.4513C46.9817 21.2521 46.8819 21.0529 46.7488 20.8868L46.9484 20.9865L47.0149 20.92L46.9151 20.6876L47.1813 20.5548L47.0815 20.4219L46.7155 20.5548L46.8486 19.9571L46.6157 19.8242L46.4161 20.2891C45.9836 19.6582 45.5179 19.0605 45.0188 18.496L46.1167 17.4998ZM51.0404 12.552C55.0325 16.7028 57.2615 22.2151 57.328 27.9598H53.4689C53.4357 25.1041 52.7703 22.2815 51.4729 19.7246L51.5061 19.6582L51.7723 19.791L51.8388 19.5918L51.1402 18.3964L50.3085 17.2673L49.3437 16.4704C49.011 16.0719 48.6783 15.6734 48.3124 15.275L51.0404 12.552ZM34.6059 51.6028C47.5805 51.6028 58.0932 41.0763 58.0599 28.1258C58.0599 16.1051 48.9445 6.04357 36.968 4.81493L36.9347 4.94776C36.9014 5.1802 36.8349 5.37944 36.8016 5.57868C41.9582 6.07677 46.7821 8.33481 50.4748 11.9543L47.8799 14.5444L47.9797 14.0795L47.647 13.9135L47.2145 13.9467L47.3143 13.6478L47.0149 12.5852L46.3828 11.8879L44.3535 10.8253L44.1871 11.0245L43.8212 11.1242C44.5198 12.1203 44.8858 13.3158 44.8858 14.5112V14.9761L45.8838 16.2379L45.4181 16.3376L45.7175 16.8024L44.8192 17.699L44.4533 17.0349C44.2869 17.4998 44.0541 17.9647 43.7879 18.3632L43.9875 18.5292L41.2263 21.2521C41.0599 21.0861 40.8936 20.9533 40.7273 20.7872C40.4611 20.92 40.195 21.0197 39.9288 21.1193L40.1617 21.2853L40.0286 21.4181L39.696 21.5842L39.5629 21.9162L39.3633 21.717L38.7977 21.9162L38.9641 22.1819L39.3633 22.0823L39.6294 22.1155L39.6627 21.9826L39.8623 21.883L39.9288 21.7834L40.2948 21.6838H40.5609L40.7273 21.8166L39.6627 22.9124L39.5962 22.8128L38.465 23.0121L38.1989 23.2777L37.966 23.3109L38.6646 22.6468L38.3985 22.514L37.7331 23.3773L37.9328 23.3441V23.6762L38.1656 23.7758L38.1989 24.1079L37.7997 24.0414L37.4005 24.1079L36.4024 23.6098C36.4024 23.6098 36.3359 26.2663 36.3359 27.5945C38.6646 28.3915 41.1598 29.5205 41.1598 32.5091C41.193 33.7709 40.5277 34.9664 39.4631 35.6637L39.3965 35.6969L39.33 35.7633C38.3985 36.3942 37.1676 36.7263 36.103 37.0584L36.0697 39.1504C37.7664 39.9805 39.7958 41.2092 39.5962 44.6626C39.5629 45.526 39.2302 45.7584 38.9641 45.8249C37.966 46.0573 36.9347 46.2233 35.9367 46.2897V47.0535C40.3281 46.7546 44.4533 44.9283 47.647 41.9065L50.375 44.6294C41.6255 53.0639 27.7527 53.0639 18.97 44.6958L21.6979 41.9729C24.8584 44.9283 28.9504 46.7214 33.2752 47.0535V46.2897C29.15 45.9577 25.2909 44.2642 22.2968 41.4084L22.9954 40.6779L23.9934 40.7775L24.5257 40.213L25.923 40.2794L26.1226 39.7813L26.0561 39.5821C28.1187 41.1428 30.5805 42.1389 33.1754 42.4046V41.6409C30.3144 41.3088 27.6529 40.1134 25.5238 38.1542L28.2517 35.4313C28.9171 36.029 29.649 36.5271 30.4807 36.9255C30.5472 36.6599 30.6138 36.4274 30.7468 36.195C30.0482 35.8297 29.3829 35.398 28.8173 34.8999L31.5453 32.177C31.9778 32.5091 32.4768 32.8079 32.9758 32.974V32.1438C32.6431 32.011 32.3437 31.8118 32.0776 31.6125L32.8427 30.8488C32.5766 30.7824 32.3104 30.6827 32.0443 30.5831L31.512 31.1144C31.2459 30.8156 31.013 30.4835 30.8467 30.1514C30.3809 29.9522 29.9151 29.7197 29.4827 29.4209C27.8858 28.4579 26.921 26.698 26.9543 24.8052C26.921 23.5434 27.287 22.2815 28.0521 21.2853L25.3242 18.5624C27.3202 16.6364 29.8819 15.4078 32.6099 14.9761V14.2123C29.6823 14.644 26.921 15.9723 24.7919 18.0311L24.3261 17.5662C24.2263 17.7322 24.0932 17.9647 23.9602 18.2635L24.2596 18.5624C21.831 21.1193 20.467 24.5063 20.4005 28.0262H16.5081C16.5747 23.4769 18.3379 19.1269 21.4983 15.8063L22.7292 17.0349H22.8956C23.1285 17.0017 23.3946 16.9353 23.5942 16.8357L22.0306 15.275C22.8623 14.478 23.7606 13.7475 24.7253 13.1165C24.7919 12.9173 24.8251 12.7181 24.9249 12.552C25.0913 12.2864 25.2909 12.0207 25.5238 11.7551C24.06 12.552 22.7292 13.5482 21.5316 14.7104L18.8036 11.9875C22.4631 8.43443 27.2204 6.2096 32.3437 5.6783C32.3437 5.57868 32.3104 5.51227 32.3104 5.51227C32.2772 5.31303 32.2439 5.147 32.2106 4.91455C19.2694 6.24281 9.92105 17.7654 11.285 30.6495C12.5492 42.5706 22.5962 51.636 34.6059 51.6028ZM46.15 11.0909L45.9171 10.7257L45.4181 10.46L45.0188 10.7589L45.5179 11.0245L46.0834 11.423L46.15 11.0909ZM43.8212 21.9826L43.8545 22.2815L44.5198 22.0823L44.7194 21.6838L44.2537 21.0861L44.4866 20.7208L45.1186 21.1525L45.2185 21.0529L45.0854 20.9533L44.9523 20.6876L45.2185 20.5548L44.9523 20.2227L44.3535 20.5216L44.1539 20.8868L44.0208 21.2189L44.2869 21.6506L44.1871 21.8498L43.8212 21.9826ZM15.9426 39.25L15.9758 39.084L15.6432 38.3202L15.2439 38.1542L15.9426 39.25ZM31.6784 24.772C31.6784 25.4361 32.0776 25.8678 32.7762 26.2663V25.9674L32.3437 25.5025L32.5766 25.0708L32.7762 25.0044C32.7429 24.2407 32.7429 23.4105 32.7429 23.2777H32.7097C32.0443 23.6762 31.7116 24.1411 31.6784 24.772Z"
                    fill="#009EDB" />
                  <path
                    d="M83.909 14.179H83.8758L81.2143 28.0593H77.5548L74.095 11.124H77.0226L79.4179 24.1741H79.4511L82.0128 11.124H85.8053L88.3337 24.1741H88.367L90.8621 11.124H93.6898L90.1967 28.0593H86.4707L83.909 14.179Z"
                    fill="#009EDB" />
                  <path
                    d="M98.2144 15.3413C100.776 15.3413 103.704 16.6696 103.704 21.7501C103.704 26.9968 100.776 28.1922 98.2144 28.1922C95.6528 28.1922 92.6919 26.9636 92.6919 21.7501C92.7252 16.6696 95.686 15.3413 98.2144 15.3413ZM98.2144 26.1002C100.144 26.1002 100.61 23.8754 100.61 21.7834C100.61 19.6913 100.177 17.4997 98.2144 17.4997C96.2516 17.4997 95.8191 19.6913 95.8191 21.7834C95.8191 23.8754 96.2848 26.1002 98.2144 26.1002Z"
                    fill="#009EDB" />
                  <path
                    d="M105.201 17.5993C105.201 16.902 105.167 16.2379 105.101 15.5405H107.829C107.862 16.3043 107.929 17.068 107.929 17.8318H107.962C108.328 16.8688 109.259 15.3745 111.156 15.3745C111.322 15.3745 111.488 15.4077 111.655 15.4409V18.2635C111.388 18.1971 111.089 18.1306 110.823 18.1306C109.592 18.1306 108.228 18.8944 108.228 21.2188V28.0594H105.234L105.201 17.5993Z"
                    fill="#009EDB" />
                  <path d="M112.852 9.8623H115.88V28.0262H112.852V9.8623Z" fill="#009EDB" />
                  <path
                    d="M128.155 9.8623V25.901C128.155 26.5983 128.189 27.3289 128.255 28.0262H125.427C125.361 27.3953 125.328 26.7312 125.328 26.1003H125.261C124.762 27.1629 123.864 28.2255 121.934 28.2255C118.84 28.2255 117.543 25.2701 117.543 21.8166C117.543 17.7322 119.173 15.3746 121.868 15.3746C123.265 15.3082 124.529 16.1051 125.095 17.367H125.128V9.8623H128.155ZM122.733 26.0006C124.496 26.0006 125.095 24.0747 125.095 21.7502C125.095 19.3261 124.429 17.5662 122.766 17.5662C121.103 17.5662 120.504 19.1933 120.504 21.6838C120.537 24.5728 121.003 26.0006 122.733 26.0006Z"
                    fill="#009EDB" />
                  <path
                    d="M137.138 11.124H140.265V17.9978H145.289V11.124H148.383V28.0593H145.289V20.5546H140.265V28.0261H137.138V11.124Z"
                    fill="#009EDB" />
                  <path
                    d="M159.428 27.4284C158.263 27.9597 156.966 28.2254 155.702 28.2254C151.676 28.2254 149.913 25.3364 149.913 21.9826C149.913 18.2635 151.876 15.3745 155.07 15.3745C157.764 15.3745 160.06 16.9352 160.06 22.049V22.6467H152.841C152.841 24.7719 153.706 26.067 156.034 26.067C157.864 26.067 158.762 25.5025 159.328 25.104L159.428 27.4284ZM157.132 20.7207C157.132 18.5291 156.4 17.4001 155.036 17.4001C153.439 17.4001 152.807 19.0604 152.807 20.7207H157.132Z"
                    fill="#009EDB" />
                  <path
                    d="M161.756 16.2711C162.987 15.6734 164.351 15.3413 165.715 15.3413C169.608 15.3413 170.506 17.2341 170.506 20.3555V25.8013C170.506 26.5319 170.572 27.2624 170.672 27.993H167.944C167.811 27.4284 167.745 26.8639 167.778 26.2994H167.745C166.979 27.3288 166.048 28.1922 164.251 28.1922C162.322 28.1922 160.525 26.8639 160.525 24.5395C160.525 21.1524 163.287 20.2891 167.112 20.2891H167.711V19.8242C167.711 18.5955 167.112 17.4333 165.383 17.4333C164.152 17.4665 162.954 17.8982 161.956 18.662L161.756 16.2711ZM167.678 21.9162H167.412C164.85 21.9162 163.32 22.4475 163.32 24.2738C163.253 25.27 164.019 26.1334 165.017 26.1998H165.249C167.046 26.1998 167.711 24.8716 167.711 22.6467V21.9162H167.678Z"
                    fill="#009EDB" />
                  <path d="M173.4 9.8623H176.395V28.0262H173.4V9.8623Z" fill="#009EDB" />
                  <path
                    d="M179.721 12.9837L182.715 12.054V15.5406H185.21V17.7323H182.715V24.2407C182.715 25.569 183.214 25.9675 184.079 25.9675C184.479 25.9675 184.878 25.8678 185.21 25.7018V27.827C184.578 28.0927 183.88 28.2255 183.181 28.2255C180.952 28.2255 179.688 27.1961 179.688 24.5728V17.7655H177.692V15.5738H179.688V12.9837H179.721Z"
                    fill="#009EDB" />
                  <path
                    d="M186.375 9.8623H189.369V17.1677H189.436C189.968 16.404 190.667 15.3746 192.53 15.3746C195.357 15.3746 196.222 17.4666 196.222 19.9903V28.0262H193.228V20.5548C193.228 18.6288 192.729 17.8318 191.498 17.8318C189.935 17.8318 189.369 19.1601 189.369 20.754V28.0262H186.375V9.8623Z"
                    fill="#009EDB" />
                  <path
                    d="M80.915 32.5422C84.4414 32.5422 87.6684 35.1655 87.6684 41.2423C87.6684 47.3191 84.4414 49.9424 80.915 49.9424C77.3886 49.9424 74.1616 47.3191 74.1616 41.2423C74.1616 35.1655 77.3886 32.5422 80.915 32.5422ZM80.915 47.5848C82.8778 47.5848 84.4747 45.9244 84.4747 41.2423C84.4747 36.5602 82.8778 34.9331 80.915 34.9331C78.9522 34.9331 77.3554 36.5934 77.3554 41.2423C77.3554 45.8912 78.9522 47.5848 80.915 47.5848Z"
                    fill="#009EDB" />
                  <path
                    d="M88.8994 39.1836C88.8994 38.4862 88.8661 37.8221 88.7996 37.1248H91.5275C91.5608 37.8885 91.6273 38.6523 91.6273 39.416H91.6606C92.0266 38.453 92.9913 36.9587 94.8543 36.9587C95.0207 36.9587 95.187 36.9919 95.3534 37.0252V39.8477C95.0872 39.7813 94.7878 39.7149 94.4884 39.7149C93.2575 39.7149 91.8935 40.4786 91.8935 42.8031V49.6436H88.8994V39.1836Z"
                    fill="#009EDB" />
                  <path
                    d="M96.8837 51.802C98.0148 52.4661 99.279 52.8314 100.576 52.8646C103.404 52.8646 103.87 50.9054 103.87 48.9462V47.7508H103.837C103.338 48.7138 102.506 49.876 100.543 49.876C98.8132 49.876 96.1851 48.7138 96.1851 43.6664C96.1851 40.2129 97.416 37.1912 100.71 37.1912C102.539 37.1912 103.371 38.2206 104.003 39.3164H104.103C104.103 38.6522 104.169 38.0213 104.203 37.3904H106.931C106.897 38.0545 106.831 38.6855 106.831 39.3496V48.5478C106.831 52.4661 105.633 55.2223 101.042 55.2223C99.5784 55.2223 98.1146 54.9566 96.7506 54.4585L96.8837 51.802ZM101.242 47.6512C103.138 47.6512 103.903 46.2897 103.903 43.4672C103.903 40.8439 102.905 39.4492 101.475 39.4824C99.8778 39.5156 99.279 40.9767 99.279 43.5004C99.279 46.4226 100.21 47.6512 101.242 47.6512Z"
                    fill="#009EDB" />
                  <path
                    d="M109.526 37.8553C110.757 37.2244 112.121 36.9255 113.484 36.9255C117.377 36.9255 118.275 38.8183 118.275 41.9397V47.3856C118.275 48.1161 118.342 48.8466 118.441 49.5772H115.713C115.58 49.0127 115.514 48.4482 115.547 47.8837H115.514C114.749 48.9131 113.817 49.7764 112.021 49.7764C110.091 49.7764 108.295 48.4482 108.295 46.1237C108.295 42.7367 111.056 41.8733 114.882 41.8733H115.481V41.4084C115.481 40.1798 114.882 39.0175 113.152 39.0175C111.921 39.0507 110.723 39.4824 109.725 40.2462L109.526 37.8553ZM115.447 43.5004H115.181C112.62 43.5004 111.089 44.0317 111.089 45.8581C111.023 46.8543 111.788 47.7176 112.786 47.784H113.019C114.815 47.784 115.481 46.4558 115.481 44.231L115.447 43.5004Z"
                    fill="#009EDB" />
                  <path
                    d="M120.837 39.1836C120.837 38.4862 120.803 37.8221 120.737 37.1248H123.565C123.598 37.7557 123.664 38.4198 123.664 39.0507H123.698C124.13 38.287 124.995 36.9587 127.024 36.9587C129.852 36.9587 130.717 39.0507 130.717 41.5744V49.6104H127.69V42.1057C127.69 40.1798 127.191 39.3828 125.96 39.3828C124.396 39.3828 123.831 40.7111 123.831 42.305V49.5772H120.837V39.1836Z"
                    fill="#009EDB" />
                  <path
                    d="M132.813 31.9114H135.941V34.8668H132.813V31.9114ZM132.88 37.2244H135.874V49.71H132.88V37.2244Z"
                    fill="#009EDB" />
                  <path
                    d="M138.469 47.1531L143.825 39.5488H138.635V37.2576H146.819V39.8145L141.563 47.4519H146.985V49.7432H138.436V47.1531H138.469Z"
                    fill="#009EDB" />
                  <path
                    d="M149.115 37.8553C150.346 37.2244 151.71 36.9255 153.074 36.9255C156.966 36.9255 157.864 38.8183 157.864 41.9397V47.3856C157.864 48.1161 157.931 48.8466 158.031 49.5772H155.303C155.17 49.0127 155.103 48.4482 155.136 47.8837H155.103C154.338 48.9131 153.406 49.7764 151.61 49.7764C149.68 49.7764 147.884 48.4482 147.884 46.1237C147.884 42.7367 150.645 41.8733 154.471 41.8733H155.07V41.4084C155.07 40.1798 154.471 39.0175 152.741 39.0175C151.51 39.0507 150.312 39.4824 149.314 40.2462L149.115 37.8553ZM155.036 43.5004H154.77C152.209 43.5004 150.678 44.0317 150.678 45.8581C150.612 46.8543 151.377 47.7176 152.375 47.784H152.608C154.404 47.784 155.07 46.4558 155.07 44.231V43.5004H155.036Z"
                    fill="#009EDB" />
                  <path
                    d="M161.091 34.5348L164.085 33.605V37.0917H166.58V39.2833H164.085V45.7585C164.085 47.0868 164.584 47.4853 165.449 47.4853C165.848 47.4853 166.247 47.4189 166.58 47.2196V49.3448C165.948 49.6437 165.249 49.7765 164.551 49.7433C162.322 49.7433 161.058 48.7139 161.058 46.1238V39.2833H159.062V37.0917H161.058L161.091 34.5348Z"
                    fill="#009EDB" />
                  <path
                    d="M168.41 31.9114H171.504V34.8668H168.41V31.9114ZM168.477 37.2244H171.504V49.71H168.51L168.477 37.2244Z"
                    fill="#009EDB" />
                  <path
                    d="M178.723 37.1912C181.285 37.1912 184.212 38.5194 184.212 43.6C184.212 48.8466 181.285 50.042 178.723 50.042C176.162 50.042 173.201 48.8466 173.201 43.6C173.234 38.5526 176.195 37.1912 178.723 37.1912ZM178.723 47.95C180.653 47.95 181.118 45.7252 181.118 43.6332C181.118 41.5412 180.686 39.3496 178.723 39.3496C176.76 39.3496 176.328 41.5412 176.328 43.6332C176.328 45.7252 176.794 47.95 178.723 47.95Z"
                    fill="#009EDB" />
                  <path
                    d="M186.707 39.1836C186.707 38.4862 186.674 37.8221 186.607 37.1248H189.435C189.468 37.7557 189.535 38.4198 189.535 39.0507H189.568C190.001 38.287 190.866 36.9587 192.895 36.9587C195.723 36.9587 196.588 39.0507 196.588 41.5744V49.6104H193.594V42.1057C193.594 40.1798 193.095 39.3828 191.864 39.3828C190.3 39.3828 189.735 40.7111 189.735 42.305V49.5772H186.74L186.707 39.1836Z"
                    fill="#009EDB" />
                </g>
                <defs>
                  <clipPath id="clip0_219_231">
                    <rect width="196.522" height="60" fill="white" transform="translate(0.739014)" />
                  </clipPath>
                </defs>
              </svg>
            </div>
            <div class="text">
              <div class="note">World Health Organization Oral Health</div>
              <a class="link" target="_blank"
                href="https://www.who.int/health-topics/oral-health">https://www.who.int/health-topics/oral-health</a>
            </div>
            <div class="text">
              <div class="small-note">Phone:</div>
              <div class="small-note text-black">+41 22 791 2111</div>
            </div>
          </div>
        </section>
        <footer>
          <div>
            <img src="https://cp-gcp-prod-osbotogilvy.web.app/assets/template/images/footer-logo.png" alt="Colgate Logo">
          </div>
          <p class="copyright">© 2024 Colgate-Palmolive Company.<br />
            All rights reserved.</p>
        </footer>
      </div>
    </div>
  </div>
  <script>
    window.addEventListener('load', function () {{
      const outer = document.querySelector('.outer')
      const container = document.querySelector('.onepage-printer')
      const printerHeight = 1080 // window.innerHeight // or any height that matches your printer
      const scale = printerHeight / outer.clientHeight
       outer.style.transform = `scale(${{scale.toFixed(2)}})`
      outer.style.transformOrigin = '50% 0'
      container.style.height = `${{printerHeight}}px`
    }})
  </script>
</body>

</html>
"""


async def render_reports(user_id, session_id):
    data_report = utils.get_user_data(user_id, session_id)
    data_report.email = utils.decrypt(data_report.email)
    data_report.phone_number = utils.decrypt(data_report.phone_number)
    # Format the HTML content with dynamic values
    logger.info(f"User input: {str(data_report.parsed_data)}")
    try:
        html_content: str = HTML_TEMPLATE.format(**data_report.parsed_data)
        pdf_path, playwright_time, playwright_memory = await utils.render_with_playwright(html_content)
        
        # Upload the generated PDF to Firebase Storage
        # Concurrently upload the generated PDF to Firebase Storage and delete the local file
        public_url = utils.upload_to_firebase(pdf_path, user_id, session_id)
        utils.delete_local_file(pdf_path)
        
        firebase.update_data_by_session_id(user_id, session_id, {"report_url": public_url})
        
        # Log performance metrics and return the result
        logger.info(f"Playwright - Time: {playwright_time:.2f}s, Memory: {playwright_memory:.2f}MB , URL: {public_url}")
        
        return {
            "playwright": {
                "time": playwright_time,
                "memory": playwright_memory
            },
            "pdf_url": public_url
        }
    except Exception as e:
        # Enhanced error handling with specific details for better debugging
        logger.debug(f"An error occurred during report rendering: {e}")
        return {}


# asyncio.run(render_reports("84389958965", "20240729114748_43c833eaf88d4abda782ce24ab6c0a2e"))
