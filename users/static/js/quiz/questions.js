$(document).ready(function() {
    $.ajax({
        method: 'GET',
        url: "/quiz/ajax_quiz/",
        dataType: 'json',
        success: function(data) {
            console.log(data.questions)
            var question = data.questions;
            var totalQuestion = question.length;
            const questions_box = document.querySelector(".questions");
            const form_box = questions_box.querySelector('#form');
            const option_list = form_box.querySelector('.option_list');
            const next_btn = document.querySelector(".next_btn");
            const bottom_ques_counter = document.querySelector(".total_que");
            const result_box = document.querySelector(".result_box");
            const quit_quiz = result_box.querySelector(".buttons .quit");
            let que_count = 0;
            let que_numb = 1;
            let userScore = 0;
            let counter;
            let counterLine;
            let widthValue = 0;
            q_length();
            showQuestions(0);
            queCounter(1);

            function q_length() {
                if (totalQuestion == 1) {
                    $("#length").text(`There is only ${totalQuestion} question in all`)
                } else if (totalQuestion > 1){
                    $("#length").text(`There are ${totalQuestion} questions in all`)
                } else if (totalQuestion == 0) {
                    $("#length").text(`There is currently no question for this subject!!`)
                }
            };

            // if quitQuiz button clicked
            quit_quiz.onclick = ()=>{
                window.location.reload(); //reload the current window
            };

            // if Next Que button clicked
            next_btn.onclick = ()=> {
                $('.result_box').hide()
                if(que_count < question.length - 1){ //if question count is less than total question length
                    que_count++; //increment the que_count value
                    que_numb++; //increment the que_numb value
                    showQuestions(que_count); //calling showQestions function
                    queCounter(que_numb); //passing que_numb value to queCounter
                } else {
                    showResult(); //calling showResult function
                }
            }

            function showQuestions(index) {
                $('.result_box').hide()
                const que_text_list = form_box.querySelector('.que_text');
                const que_num = form_box.querySelector('.que_num');

                let que_tag = '<h3>'+question[index].question+'</h3>'+'<br>';
                let option_tag = '<div class="option"><span>'+question[index].option1+'</span></div>'
                +'<div class="option"><span>'+question[index].option2+'</span></div>'
                +'<div class="option"><span>'+question[index].option3+'</span></div>'
                +'<div class="option"><span>'+question[index].option4+'</span></div>';

                //que_num.innerHTML = '<h4>Question '+ index+1 +'</h4>'
                que_num.innerHTML = `<h4>Question ${index+1}</h4>`

                que_text_list.innerHTML = que_tag;
                option_list.innerHTML = option_tag;
                $('.questions').show();
                $('.option').click(function () {
                    $(this).on('click', optionSelected(this))
                })
            }

            // creating the new div tags which for icons
            let tickIconTag = '<div class="icon tick"><i class="fa fa-check" aria-hidden="true"></i></i></div>';
            let crossIconTag = '<div class="icon cross"><i class="fa fa-times" aria-hidden="true"></i></div>';


            //if user clicked on option
            function optionSelected(ans){
                let userAns = ans.textContent; //getting user selected option
                let correcAns = question[que_count].answer; //getting correct answer from array
                const allOptions = option_list.children.length; //getting all option items

                if(userAns == correcAns){ //if user selected option is equal to array's correct answer
                    userScore += 1; //upgrading score value with 1
                    ans.classList.add("correct"); //adding green color to correct selected option
                    ans.insertAdjacentHTML("beforeend", tickIconTag); //adding tick icon to correct selected option
                }else{
                    ans.classList.add("incorrect"); //adding red color to correct selected option
                    ans.insertAdjacentHTML("beforeend", crossIconTag); //adding cross icon to correct selected option

                    for(i=0; i < allOptions; i++){
                        if(option_list.children[i].textContent == correcAns){ //if there is an option which is matched to an array answer 
                            option_list.children[i].setAttribute("class", "option correct"); //adding green color to matched option
                            option_list.children[i].insertAdjacentHTML("beforeend", tickIconTag); //adding tick icon to matched option
                        }
                    }
                }
                
                for(i=0; i < allOptions; i++){
                    option_list.children[i].classList.add("disabled"); //once user select an option then disabled all options
                }
                $('.footer').show();
            }

            function showResult(){
                $('.result_box').show()                        
                const scoreText = result_box.querySelector(".score_text");
                //creating a new span tag and passing the user score number and total question number
                let scoreTag = '<h2>You got <strong>'+ userScore +'</strong> out of <strong>'+ question.length +'</strong></h2>';
                scoreText.innerHTML = scoreTag;  //adding new span tag inside score_Text
            }

            function queCounter(index){
                //creating a new span tag and passing the question number and total question
                let totalQueCounTag = '<span>Question '+ index +' of '+ question.length +'</span>';
                bottom_ques_counter.innerHTML = totalQueCounTag;  //adding new span tag inside bottom_ques_counter
            }


        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    })
})