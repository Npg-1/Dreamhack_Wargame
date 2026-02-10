const questionView = document.querySelector('.questionView')    // document에서 class = questionView를 questionView에 할당, questionView가 가장 바깥 컨테이너임
const chapter = questionView.querySelector('.chapter')          // questionView에서 chapter 클래스를 가진 요소를 가져옴
const questionImage = questionView.querySelector('img')         // questionView에서 img 태그를 가진 요소를 가져옴
const submitButton = questionView.querySelector('.submitButton')

const successView = document.querySelector('.successView')
const flag = successView.querySelector('.flag')

const failView = document.querySelector('.failView')
const questionRow = failView.querySelector('.questionRow')

/*
    [솔리데오SI시스템즈 Mr.Hwang 20050624]
    관리자의 설정으로만 재응시 가능하게 수정
*/
// const resetButton = failView.querySelector('.resetButton')

const spinner = document.querySelector('.spinner')

let currentQuestionId = null
async function next(body) {
    spinner.classList.remove('d-none')
    questionView.classList.add('d-none')
    successView.classList.add('d-none')
    failView.classList.add('d-none')
    const data = await fetch('/next', {
        method: 'post',
        body: JSON.stringify(body || {}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    spinner.classList.add('d-none')
    if (data.finished) {
        if (data.incorrectQuestions.length === 0) {
            successView.classList.remove('d-none')
            flag.textContent = data.flag
        } else {
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
    } else if (data.question) {
        questionView.classList.remove('d-none')
        chapter.textContent = `${data.count + 1}. ${data.question.chapter || ''}`
        questionImage.src = data.question.questionImage
        currentQuestionId = data.question.id
    } else if (data.error) {
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
// resetButton.addEventListener('click', async () => {
//     await fetch('/reset', {
//         headers: {
//             'dev-auth': '1q2w3e4r_solideo!!'
//         }
//     })
//     location.reload()
// })

next()