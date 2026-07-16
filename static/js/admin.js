const ctx = document.getElementById("statusChart");

new Chart(ctx, {
    type: "doughnut",

    data: {
        labels: ["Read", "Unread"],

        datasets: [{
            data: [
                Number(document.getElementById("readCount").value),
                Number(document.getElementById("unreadCount").value)
            ],

            backgroundColor: [
                "#22c55e",
                "#ef4444"
            ]
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});