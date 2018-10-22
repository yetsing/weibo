// WEIBO API

var apiWeiboAll = function(callback) {
    var path = '/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weiboId, callback) {
    var path = `/weibo/delete?id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/weibo/update'
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo, username) {
    var created_time = fromNow(weibo.created_time)
    var updated_time = formatUnixTimestamp(weibo.updated_time)
    var button = ''
    if (username == weibo.username) {
        var button = `
        <a href="javascript:void(0);" data-action="deleteWeibo" class="weibo-delete" style="font-size: smaller">删除</a>
        <a href="javascript:void(0);" data-action="editWeibo" class="weibo-edit" style="font-size: smaller">编辑</a>
        `
    }

    var t = `
        <section class="post weibo-cell" data-id="${weibo.id}">
            <header class="post-header">
                <img width="48" height="48" alt="${weibo.username}" class="post-avatar" src="/static/images/default.jpg">
                <p class="post-meta">
                    <a href="javascript:void(0);" class="post-author" style="font-size: large; font-weight: bolder;">${weibo.username}</a>
                     · 创建于
                    <a href="javascript:void(0);" style="color: #8590a6;">
                        ${created_time}
                    </a>
                    ${button}
                </p>
            </header>
            <div class="post-description">
                <p class="weibo-content">${weibo.content}</p>
            </div>
            <div>
                <a href="javascript:void(0);" data-action="loadComments" class="weibo-comment-all">
                    <span class="weibo-comment-count">${weibo.comment_count}</span>
                    条评论
                </a>
                <span class="weibo-time">编辑于
                    <span class="weibo-updated-time">${updated_time}</span>
                </span>
            </div>
        </section>
        <h1 id="id-line-${weibo.id}" class="content-subhead update-form"> </h1>
    `
    return t
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form pure-form pure-form-stacked">
            <textarea class="weibo-update-input" rows="5" style="width: 100%">${content}</textarea>
            <button data-action="updateWeibo" class="weibo-update pure-button pure-button-primary">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo, username) {
    var weiboCell = weiboTemplate(weibo, username)
    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('afterbegin', weiboCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(weibos) {
        // 循环添加到页面中
        var username = weibos.pop(-1).username
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo, username)
        }
    })
}

var addWeibo = function(event) {
    var input = e('#id-input-weibo')
    var content = input.value
    var form = {
        content: content,
    }
    apiWeiboAdd(form, function(weibo) {
        // 收到返回的数据, 插入到页面中
        insertWeibo(weibo, weibo.username)
        input.value = ''
    })
}

var deleteWeibo = function(event) {
    var self = event.target
    var weiboCell = self.closest('.weibo-cell')
    var weiboId = weiboCell.dataset['id']
    apiWeiboDelete(weiboId, function(r) {
        var line = e(`#id-line-${weiboId}`)
        weiboCell.remove()
        line.remove()
        alert(r.message)
    })
}

var editWeibo = function(event) {
    var self = event.target
    if (self.classList.contains('weibo-active')) {
        self.classList.remove('weibo-active')
        var weiboCell = self.closest('.weibo-cell')
        var weiboUpdateForm = e('.weibo-update-form', weiboCell)
        weiboUpdateForm.remove()
    } else if (self.classList.contains('weibo-edit')) {
        self.classList.add('weibo-active')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var postDescription = e('.post-description', weiboCell)
        var weiboSpan = e('.weibo-content', weiboCell)
        var content = weiboSpan.innerText
        // 插入编辑输入框
        insertUpdateForm(content, postDescription)
    }
}

var updateWeibo = function(event) {
    var self = event.target
    weiboCell = self.closest('.weibo-cell')
    weiboId = weiboCell.dataset['id']
    input = e('.weibo-update-input', weiboCell)
    content = input.value
    var form = {
        id: weiboId,
        content: content,
    }

    apiWeiboUpdate(form, function(weibo) {
        var weiboSpan = e('.weibo-content', weiboCell)
        weiboSpan.innerText = weibo.content
        var weiboUpdatedTime = e('.weibo-updated-time', weiboCell)
        weiboUpdatedTime.innerText = formatUnixTimestamp(weibo.updated_time)

        var updateForm = e('.weibo-update-form', weiboCell)
        updateForm.remove()
        var editButton = e('.weibo-edit', weiboCell)
        editButton.classList.remove('active')
    })
}

var __main = function() {
    loadWeibos()
}

__main()
