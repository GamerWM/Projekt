if (!window.dash_clientside) {
    window.dash_clientside = {};
}
console.log("Test");
window.dash_clientside.clientside = {
    changeWidth: function() {
        console.log("Test1");
        var allSideElements = document.querySelectorAll('#all-side, #all-side-2');
        allSideElements.forEach(function(element) {
            console.log("Test2");
            element.style.width = '50%';
        });
        return window.dash_clientside.no_update;
    }
}