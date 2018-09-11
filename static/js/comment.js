var apiWeiboCommentAdd = function(form, callback) {
    var path = '/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboCommentDelete = function(comment_id, callback) {
    var path = `/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboCommentUpdate = function(form, callback) {
    var path = '/comment/update'
    ajax('POST', path, form, callback)
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

var insertWeiboComment = function(comment, weiboCommentList) {
    var t = `
        <div class="weibo-comment-cell" data-id="${comment.id}">
            <span>${comment.username}: </span>
            <span class="weibo-comment-content">${comment.content}</span>
            <button class="weibo-comment-edit">编辑</button>
            <button class="weibo-comment-delete">删除</button>
        </div>
    `
    weiboCommentList.insertAdjacentHTML('beforeend', t)
}

var insertCommentUpdateForm = function(content, weiboCommentCell) {
    var updateForm = weiboCommentUpdateTemplate(content)
    weiboCommentCell.insertAdjacentHTML('beforeend', updateForm)
}

var bindEventWeiboCommentAdd = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-comment-add')) {
        log('点到了添加评论按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        var weiboCommentList = e('.weibo-comment-list', weiboCell)
        var input = e('.weibo-comment-input', weiboCell)
        var content = input.value
        log('添加评论', content)
        var form = {
            weibo_id: weiboId,
            content: content,
        }
        apiWeiboCommentAdd(form, function(comment) {
            // 收到返回的数据, 插入到页面中
            insertWeiboComment(comment, weiboCommentList)
            input.value = ''
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-comment-delete')) {
        log('点到了 comment 删除按钮')
        weiboCommentCell = self.closest('.weibo-comment-cell')
        commentId = weiboCommentCell.dataset['id']
        apiWeiboCommentDelete(commentId, function(r) {
            log('apiWeiboCommentDelete', r.message)
            // 删除 self 的父节点
            self.parentElement.remove()
            alert(r.message)
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-comment-edit')) {
        log('点到了 comment 编辑按钮')
        weiboCommentCell = self.closest('.weibo-comment-cell')
        commentId = weiboCommentCell.dataset['id']
        var commentSpan = e('.weibo-comment-content', weiboCommentCell)
        var content = commentSpan.innerText
        // 插入编辑输入框
        insertCommentUpdateForm(content, weiboCommentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-comment-update')) {
        log('点到了 comment 更新按钮')
        weiboCommentCell = self.closest('.weibo-comment-cell')
        commentId = weiboCommentCell.dataset['id']
        log('update weibo comment id', commentId)
        input = e('.weibo-comment-update-input', weiboCommentCell)
        content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiWeiboCommentUpdate(form, function(comment) {
            // 收到返回的数据, 插入到页面中
            log('apiWeiboCommentUpdate', comment)

            var commentSpan = e('.weibo-comment-content', weiboCommentCell)
            commentSpan.innerText = comment.content

            var updateForm = e('.weibo-comment-update-form', weiboCommentCell)
            updateForm.remove()
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var __main = function() {
    bindEventWeiboCommentAdd()
    bindEventWeiboCommentDelete()
    bindEventWeiboCommentEdit()
    bindEventWeiboCommentUpdate()
}

__main()