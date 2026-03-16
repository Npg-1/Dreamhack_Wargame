const questionView = document.querySelector('.questionView')    // document에서 class = questionView를 questionView에 할당, questionView가 가장 바깥 컨테이너임
const chapter = questionView.querySelector('.chapter')          // questionView에서 chapter 클래스를 가진 요소를 가져옴
const questionImage = questionView.querySelector('img')         // questionView에서 img 태그를 가진 요소를 가져옴
const submitButton = questionView.querySelector('.submitButton')

const successView = document.querySelector('.successView')
const flag = successView.querySelector('.flag')

const failView = document.querySelector('.failView')
const questionRow = failView.querySelector('.questionRow')

const resetButton = failView.querySelector('.resetButton')      // resetButton 요소를 html에서 가져오기

const spinner = document.querySelector('.spinner')

let currentQuestionId = null
async function next(body) {
    // classList는 요소의 클래스를 나타내는 것으로 classList.remove('d-none')는 요소의 클래스인 d-none을 삭제하게 됨
    spinner.classList.remove('d-none')      // 여기서 말하는 d-none은 display: none 으로 remove를 했으니까 spinner 요소가 나타남
    questionView.classList.add('d-none')    // 여기선 d-none을 추가했으니까  questionView가 안 보임
    successView.classList.add('d-none')     // successView 안 보임
    failView.classList.add('d-none')        // failView 안 보임

    const data = await fetch('/next', {     // '/next'라는 주소로 body를 JSON형식으로 POPT 요청함
        method: 'post',
        body: JSON.stringify(body || {}),
        headers: {                          // 보내는 데이터가 JSON 형식이라는 걸 표시
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())              // 서버의 응답을 받아오면 받아온 응답(res)를 json으로 바꿔서 data에 저장

    spinner.classList.add('d-none')         

    if (data.finished) {                    // 서버에서 받아온 데이터에서 finished가 True라면
        if (data.incorrectQuestions.length === 0) {         // 틀린 문제가 없다면, -> 모든 문제를 다 맞췄다면 플래그 출력
            successView.classList.remove('d-none')
            flag.textContent = data.flag
        } else {                                            // 1개 이상 틀린 문제가 있다면 
            failView.classList.remove('d-none')               
            let index = 1
            for (const questionData of data.incorrectQuestions) {
                const questionElement = document.createElement('div')
                questionElement.classList.add('col-6', 'col-xl-3', 'pt-5')
                questionElement.innerHTML = `
                    <p class="fw-bold">${index++}. ${questionData.chapter || ''}</p>
                    <img src="${questionData.questionImage}" alt="문제 이미지" class="w-100" loading="lazy">
                `
                questionRow.appendChild(questionElement)
            }
        }
    } 
    else if (data.question) {   // 문제를 다 못 풀었다면
        questionView.classList.remove('d-none')     // 문제 표시
        chapter.textContent = `${data.count + 1}. ${data.question.chapter || ''}`
        questionImage.src = data.question.questionImage
        currentQuestionId = data.question.id        // 현재 문제 번호를 받아온 응답의 문제 번호로 기입함
    } 
    else if (data.error) {
        alert(data.error)
        location.reload()
    }
}

submitButton.addEventListener('click', () => {
    const answer = questionView.querySelector('input[name=questionRadio]:checked')?.value
    if (!answer) return alert('답변을 선택해주세요.')
    next({
        questionId: currentQuestionId,
        answer: parseInt(answer)
    })
    questionView.querySelector('input[name=questionRadio]:checked').checked = false
})



/*
    [솔리데오SI시스템즈 Mr.Hwang 20050624]
    관리자의 설정으로만 재응시 가능하게 수정
*/



const data = await fetch('/next', {     // '/next'라는 주소로 body를 JSON형식으로 POPT 요청함
    method: 'post',
    body: JSON.stringify(body || {}),
    headers: {                          // 보내는 데이터가 JSON 형식이라는 걸 표시
        'Content-Type': 'application/json'
    }
}).then(res => res.json())              // 서버의 응답을 받아오면 받아온 응답(res)를 json으로 바꿔서 data에 저장



resetButton.addEventListener('click', async () => {
    await fetch('/reset', { headers: { 'dev-auth': '1q2w3e4r_solideo!!' } })
    location.reload()
})



next()      // index.js가 처음 호출될 때 next()도 한 번은 호출하게 됨