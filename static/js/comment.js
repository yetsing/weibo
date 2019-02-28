// Comment API

var apiWeiboCommentAll = function(weiboId, callback) {
    var path = `/comment/all?weibo_id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboCommentAdd = function(form, callback) {
    var path = '/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboCommentDelete = function(commentId, callback) {
    var path = `/comment/delete?id=${commentId}`
    ajax('GET', path, '', callback)
}

var apiWeiboCommentUpdate = function(form, callback) {
    var path = '/comment/update'
    ajax('POST', path, form, callback)
}

var commentTemplate = function(comment, username) {
    var created_time = fromNow(comment.created_time)
    var button = ''
    if (username == comment.username) {
        var button = `
        <a href="javascript:void(0);" data-action="deleteComment" class="weibo-comment-delete" style="font-size: xx-small">删除</a>
        `
    }
    var t = `
        <div class="weibo-comment-cell" data-id="${comment.id}">
            <div style="margin-left: 12px; margin-bottom: 10px;">
                <span style="color: rgb(61, 146, 201); font-weight: bolder;">${comment.username}</span>
                ${button}
                <span style="float: right; color: #8590a6; margin-right: 10px;">${created_time}</span>
            </div>
            <div style="margin-left: 12px;">
                ${comment.content}
            </div>
            <h1 class="content-subhead update-form"> </h1>
        </div>
    `
    return t
}

var weiboCommentUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-comment-update-form">
            <input class="weibo-comment-update-input" value="${content}">
            <button class="weibo-comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeiboComment = function(comment, username, weiboCommentList) {
    var commentCell = commentTemplate(comment, username)
    weiboCommentList.insertAdjacentHTML('afterbegin', commentCell)
}

var insertWeiboCommentList = function(weiboCommentList, weiboCell) {
    var weiboComments = `
    <div class="weibo-comment-list">
        ${weiboCommentList}
        <div class="weibo-comment-add-form pure-form" style="margin: 10px;">
            <input class="weibo-comment-input" placeholder="写下你的评论..." style="width: 80%; height: 30px;">
            <button data-action="addComment" class="weibo-comment-add pure-button pure-button-primary">评论</button>
        </div>
    </div>
    `
    weiboCell.insertAdjacentHTML('beforeend', weiboComments)
}

var insertCommentUpdateForm = function(content, weiboCommentCell) {
    var updateForm = weiboCommentUpdateTemplate(content)
    weiboCommentCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadComments = function(event) {
    var self = event.target
    if (self.classList.contains('active')) {
        self.classList.remove('active')
        var weiboCell = self.closest('.weibo-cell')
        var weiboCommentList = e('.weibo-comment-list', weiboCell)
        weiboCommentList.remove()
    } else if (self.classList.contains('weibo-comment-all')) {
        self.classList.add('active')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']

        apiWeiboCommentAll(weiboId, function(comments) {
            // 循环添加到页面中
            var username = comments.pop().username
            var weiboCommentList = ''
            for(var i = 0; i < comments.length; i++) {
                var comment = comments[i]
                weiboCommentList += commentTemplate(comment, username)
            }
            insertWeiboCommentList(weiboCommentList, weiboCell)
        })
    }
}

var addComment = function(event) {
    var self = event.target
    var weiboCell = self.closest('.weibo-cell')
    var weiboId = weiboCell.dataset['id']
    var weiboCommentList = e('.weibo-comment-list', weiboCell)
    var input = e('.weibo-comment-input', weiboCell)
    var content = input.value
    var form = {
        weibo_id: weiboId,
        content: content,
    }

    apiWeiboCommentAdd(form, function(comment) {
        // 收到返回的数据, 插入到页面中
        insertWeiboComment(comment, comment.username, weiboCommentList)
        input.value = ''
        var weiboCommentCount = e('.weibo-comment-count', weiboCell)
        var count = Number(weiboCommentCount.innerText) + 1
        weiboCommentCount.innerText = count
    })
}

var deleteComment = function(event) {
    var self = event.target
    var weiboCommentCell = self.closest('.weibo-comment-cell')
    var commentId = weiboCommentCell.dataset['id']

    apiWeiboCommentDelete(commentId, function(r) {
        var weiboCell = self.closest('.weibo-cell')
        weiboCommentCell.remove()
        var weiboCommentCount = e('.weibo-comment-count', weiboCell)
        var count = Number(weiboCommentCount.innerText) - 1
        weiboCommentCount.innerText = count
        alert(r.message)
    })
}
