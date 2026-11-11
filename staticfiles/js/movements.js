



function applyFilterTabe(selectedMonth) {
    const rowsFees = document.querySelectorAll('.table-Fees-Movements');
    const rowsMovements = document.querySelectorAll('.table-Income');
    const rowsExpenses = document.querySelectorAll('.table-expense');

    let totalIncome = 0;
    let totalExpenses = 0;

    const filterRows = (rows, callback) => {
        rows.forEach(row => {
            const rowMonth = row.dataset.month;

            if (selectedMonth === "" || rowMonth === selectedMonth) {
                row.style.display = "";
                callback(Number(row.dataset.value || 0));
            } else {
                row.style.display = "none";
            }
        });
    };

    filterRows(rowsFees, value => {
        totalIncome += value;
    });

    filterRows(rowsMovements, value => {
        totalIncome += value;
    });

    filterRows(rowsExpenses, value => {
        totalExpenses += value;
    });

    const balance = totalIncome - totalExpenses;

    const formatter = new Intl.NumberFormat('pt-PT', {
        style: 'currency',
        currency: 'EUR'
    });

    document.getElementById('totalIncome').textContent = formatter.format(totalIncome);
    document.getElementById('totalExpenses').textContent = formatter.format(totalExpenses);
    document.getElementById('balance').textContent = formatter.format(balance);
}

document.getElementById('filterMonth').addEventListener('change', function() {
    applyFilterTabe(this.value);
});

document.addEventListener('DOMContentLoaded', function() {
    applyFilterTabe(document.getElementById('filterMonth').value);
});



document.getElementById('filterMonth').addEventListener("change", function(){
    const selectedMonth = this.value
    console.log(selectedMonth)

    applyFilterTabe(selectedMonth)
    

    
})


const currentDate = new Date();
    const months = [
        "January", "February", "March", "April", "May", "June", "July", 
        "August", "September", "October", "November", "December"
    ];
    
const currentMonth = months[currentDate.getMonth()];
const currentYear = currentDate.getFullYear();

const currentMonthYear = `${currentMonth} ${currentYear}`;
console.log(currentMonthYear)
    

    // Selecionar o <select> e definir a opção correta como selecionada
const filterMonthSelect = document.getElementById("filterMonth");
for (const option of filterMonthSelect.options) {
    if (option.value === currentMonthYear) {
        console.log(option.value)
        option.selected = true;
        applyFilterTabe(currentMonthYear)
        break;
        }
    }


function deleteMovement(id, description){
    if (confirm(`Tem certeza que deseja excluir o movimento "${description}"?`)) {
        console.log(`/financeManagment/delete_movements/${id}`)
        window.location.href = `/finance/delete_movements/${id}/`;
    }
}