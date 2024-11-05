document.getElementById('filterMonth').addEventListener("change", function(){
    const selectedMonth = this.value
    

    const rows = document.querySelectorAll("#tableMontlyPayments")

    rows.forEach(row => {
        const rowMonth = row.getAttribute("data-month")

        if (selectedMonth === "" || rowMonth === selectedMonth){
            row.style.display = "";
        }else {
            row.style.display = 'none'
        }
    })
})

const currentDate = new Date();
    const months = [
        "January", "February", "March", "April", "May", "June", "July", 
        "August", "September", "October", "November", "December"
    ];
    
    const currentMonth = months[currentDate.getMonth()];
    const currentYear = currentDate.getFullYear();

    // Formatar o valor no formato esperado, ex: "October 2024"
    const currentMonthYear = `${currentMonth} ${currentYear}`;
    console.log(currentMonthYear)

    // Selecionar o <select> e definir a opção correta como selecionada
    const filterMonthSelect = document.getElementById("filterMonth");
    for (const option of filterMonthSelect.options) {
        if (option.value === currentMonthYear) {
            console.log(option.value)
            option.selected = true;
            
            break;
        }
    }