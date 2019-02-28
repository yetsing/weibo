var actions = {
    // weibo event
    addWeibo,
    deleteWeibo,
    editWeibo,
    updateWeibo,
    // comment event
    loadComments,
    addComment,
    deleteComment,
}

var bindEvents = function() {
    e('body').addEventListener('click', event => {
        let action = event.target.dataset.action
        actions[action] && actions[action](event)
    })
}

var __main = function() {
    loadWeibos()
    bindEvents()
}

__main()
