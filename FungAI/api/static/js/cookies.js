if (!document.cookie.includes('cookiesAccepted=true')) {
    document.getElementById('cookie-banner').style.display = 'block';
}

document.getElementById('accept-all').addEventListener('click', function () {
    document.cookie = "cookiesAccepted=true; path=/; max-age=" + 60 * 60 * 24 * 365;
    document.getElementById('cookie-banner').style.display = 'none';
});

document.getElementById('accept-necessary').addEventListener('click', function () {
    document.cookie = "cookiesAccepted=necessary; path=/; max-age=" + 60 * 60 * 24 * 365;
    document.getElementById('cookie-banner').style.display = 'none';
});
