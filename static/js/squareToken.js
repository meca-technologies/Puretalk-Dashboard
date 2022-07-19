const sat = 'EAAAEBn_K2QBKzBQqjB3-XL2haWsArbenp2FsdlAVEgVCwK3WAhWKI9eh1E_wnwg';
const ai = 'sandbox-sq0idb-uws6TNoLPsugi8xwgPL8HQ';
const lid = 'L42VTHW1N9MCQ'
async function initializeCard(payments) {
    const card = await payments.card();
    await card.attach('#card-container');
    return card;
}

// Call this function to send a payment token, buyer name, and other details
// to the project server code so that a payment can be created with 
// Payments API
async function createPayment(token, use_coff=false) {
    var save_card = document.getElementById("square-save-card").checked;
    console.log(save_card);
    var body = {
        lid,
        sourceId: token,
        use_coff:use_coff,
        save_card:save_card,
        company_id:$("#company-body").val(),
        amount:$("#square-amount").val(),
    };
    document.getElementById("payment-body-square").style.display = "none";
    document.getElementById("square-loading-bar").style.display = "";

    $("#card-button").prop( "disabled", true );

    postToAPI('/api/v1/square/charge', body, 'POST', 'updateWalletCharge');
}

// This function tokenizes a payment method. 
// The ‘error’ thrown from this async function denotes a failed tokenization,
// which is due to buyer error (such as an expired card). It is up to the
// developer to handle the error and provide the buyer the chance to fix
// their mistakes.
async function tokenize(paymentMethod) {
    const tokenResult = await paymentMethod.tokenize();
    if (tokenResult.status === 'OK') {
        return tokenResult.token;
    } else {
        let errorMessage = `Tokenization failed-status: ${tokenResult.status}`;
        if (tokenResult.errors) {
            errorMessage += ` and errors: ${JSON.stringify(
            tokenResult.errors
        )}`;
        }
        throw new Error(errorMessage);
    }
}

// Helper method for displaying the Payment Status on the screen.
// status is either SUCCESS or FAILURE;
function displayPaymentResults(status) {
    const statusContainer = document.getElementById(
        'payment-status-container'
    );
    if (status === 'SUCCESS') {
        statusContainer.classList.remove('is-failure');
        statusContainer.classList.add('is-success');
    } else {
        statusContainer.classList.remove('is-success');
        statusContainer.classList.add('is-failure');
    }

    statusContainer.style.visibility = 'visible';
}

document.addEventListener('DOMContentLoaded', async function() {
    if (!window.Square) {
        throw new Error('Square.js failed to load properly');
    }
    const payments = window.Square.payments(ai, lid);
    let card;
    try {
        card = await initializeCard(payments);
    } catch (e) {
        console.error('Initializing Card failed', e);
        return;
    }

    async function handlePaymentMethodSubmission(event, paymentMethod) {
        var use_coff = document.getElementById("square-create-card-body").classList.contains('d-none');
        if(use_coff){
            var coffs = document.getElementsByClassName("square-payment-coff");
            for(var i = 0; i<coffs.length; i++){
                console.log(coffs[i].checked);
                if(coffs[i].checked){
                    createPayment($(coffs[i]).attr('card-id'), true);
                }
            }
        }
        else{        
            event.preventDefault();

            try {
                // disable the submit button as we await tokenization and make a
                // payment request.
                cardButton.disabled = true;
                const token = await tokenize(paymentMethod);
                const paymentResults = await createPayment(token);
                displayPaymentResults('SUCCESS');
    
                console.debug('Payment Success', paymentResults);
            } catch (e) {
                cardButton.disabled = false;
                displayPaymentResults('FAILURE');
                console.error(e.message);
            }
        }
    }

    const cardButton = document.getElementById(
        'card-button'
    );
    cardButton.addEventListener('click', async function(event) {
        await handlePaymentMethodSubmission(event, card);
    });
});
function updateWalletCharge(){
    $("#add-funds").modal('hide');
    getTransactions($('#company-body'));
    document.getElementById("payment-body-square").style.display = "";
    document.getElementById("square-loading-bar").style.display = "none";

    $("#card-button").prop( "disabled", false );
}