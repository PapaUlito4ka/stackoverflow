

function updateQuestionVotes (question_id, selector) {
    let value = parseInt($('.question-votes').text());
    if (selector === 'down') value--;
    else value++;
    $.ajax({
        url: `http://localhost:8000/api/question/${question_id}/votes`,
        type: 'PUT',
        data: JSON.stringify({ votes: value }),
        beforeSend: function(xhr){xhr.setRequestHeader('token', `^9%-g9b&lpgeq-&j)r40qc%v5sr!!idxm333r6&utg(f80@mqj`);},
        success: function (json) {
            json = $.parseJSON(json);
            $('.question-votes').text(($.parseJSON(json.data)).votes);
        }
    })
}

function updateAnswerVotes (answer_id, selector) {
    let value = parseInt($(`.answer-likes-${answer_id}`).text());
    if (selector === 'down') value--;
    else value++;
    $.ajax({
        url: `http://localhost:8000/api/answer/${answer_id}/likes`,
        type: 'PUT',
        data: JSON.stringify({ likes: value }),
        beforeSend: function(xhr){xhr.setRequestHeader('token', `^9%-g9b&lpgeq-&j)r40qc%v5sr!!idxm333r6&utg(f80@mqj`);},
        success: function (json) {
            json = $.parseJSON(json);
            $(`.answer-likes-${answer_id}`).text(($.parseJSON(json.data)).likes);
        }
    })
}


