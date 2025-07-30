document.querySelector('.btn-download').addEventListener('click', function(e) {
    e.preventDefault();
    alert('正在准备下载...请稍候');
    // 3秒后开始下载
    setTimeout(function() {
        window.location.href = 'm.py';
    }, 3000);
});