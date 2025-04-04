
// Show loader message
function showLoaderMessage(message) {
    const loaderHtml = `
        <div class="w-100 text-center p-2" id="loader">
            <span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span>
            <span class="m-3">${message}</span>
        </div>`;
    $("#trans_progress").html(loaderHtml).hide().fadeIn(1500);
}

// Update the status message
function updateMessage(message) {
    $('#message').html(`<p class="text-right align-items-center text-danger"><b>${message}</b></p>`);
}

function Refresh(){
    window.location.reload();
}

function onBypassClick(){
    console.log("bypass clicked")
    }

function onSubmitClick() {

    if($('#gcb_type').val() == "00"){  $('#GcbTypeP').text("Select Entry Mode"); } else {  $('#GcbTypeP').text("") }
    if($('#token_type').val() == "00"){  $('#TokenTypeP').text("Select Token") } else {  $('#TokenTypeP').text("") }
    if($('#Transaction_Type').val() == "00"){  $('#TransactionTypeP').html("Select Transaction") }  else {  $('#TransactionTypeP').text("") }
    if($('#itr').val() == ""){  $('#itrP').html("Enter Iterations") }  else {  $('#itrP').text("") }
    $('#itr').prop('disabled', true);
    $('#submit').prop('disabled', true);
    $('#Transaction_Type').prop('disabled', true);
    $('#myTable').removeClass('d-none');
    if($('#gcb_type').val()  != "00" && $('#token_type').val()  != "00" && $('#Transaction_Type').val()  != "00"){
    table_header = $('<tr id="head1"><th>Token</th><th>TestCard</th><th>Request</th><th>EntryMode</th><th>TransType</th><th>CardType</th><th>SubCardType</th><th>TrnsAmt</th><th>ApprovedAmt</th><th>ResponseText</th><th>ResponseCode</th><th>TransactionID</th><th>AurusPayTicketNum</th><th>ApprovalCode</th></tr>').hide();
    $("#table_header").html(table_header);
    $(table_header).fadeIn("slow");
        setTimeout(function() {
            BindConnection();
        }, 0);
    }
    finalizeUI();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function switchBtn() {
    $(".panel-wrap").toggleClass("panel-unwrap");
    $(".sidepanel").toggleClass("sidepanel-unwrap");
    icon = $(this).find("i");
    if (icon.hasClass("fa-plus")) {
        icon.addClass("fa-minus").removeClass("fa-plus");
    } else {
        icon.addClass("fa-plus").removeClass("fa-minus");
    }
}

function getRandomNumber(min, max, decimalPlaces) {
  // Generate a random number between min (inclusive) and max (exclusive)
  let randomInteger = Math.floor(Math.random() * (max - min + 1)) + min;

  // Format the number with ".00" appended
  return randomInteger + ".00";

  }

function before_data_send(i, message) {
    $('#loader').show();
    a = $('<div id="img">Icon</div><div id="desc">A notification message..</div>').hide();
    str = $('<div class="p-1"><div class="spinner-border text-white" role="status" style="vertical-align: middle;"></div><span class="text-center m-5"># ' + i +' '+message+'</span></div>').hide();
    $("#trans_progress").html(str);
    $(str).fadeIn(1000);
}

function exportToExcel(id, par1, par2) {
    if(id === "0"){ //instore Testing
        let currentDate = new Date();
        var par1 = currentDate.toISOString().slice(0, 10);
        var par2 = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
        par1.replace("-", "");
        par2.replace("_", "");
        fileName =  'Instore_testing_' + par1 + '_' + par2 + '.xlsx'
    }
    if(id === "1"){ // Dual Processor
        if(par2 === "1"){
            processor = "Chase"
        }else{
            processor = "Worldpay"
        }
        amount = "100."+par1
        fileName = 'DualProcessor_testing_' + processor + '_' + amount + '.xlsx'
    }
     if(id === "2"){ //instore Testing
        let currentDate = new Date();
        var par1 = currentDate.toISOString().slice(0, 10);
        var par2 = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
        par1.replace("-", "");
        par2.replace("_", "");
        fileName =  'SequenceValidation' + par1 + '_' + par2 + '.xlsx'
    }
    let table = document.getElementsByTagName("table"); // you can use document.getElementById('tableId') as well by providing id to the table tag
    TableToExcel.convert(table[0], { // html code may contain multiple tables so here we are refering to 1st table tag
        name: fileName, // fileName you could use any name
        sheet: {
            name: 'Testing_Result' // sheetName
        }
    });
}

function chaseProcessorResponseCode(code){
    responsecodes =  {
    "00": "Approved authorization or transaction",
    "01": "Refer to card issuer",
    "02": "Refer to card issuer's special conditions",
    "03": "Invalid merchant or terminal",
    "04": "Pick up",
    "05": "Do not honor Note: If this error code was returned on a Mastercard transaction attempted at the point of sale in Europe, the merchant must request additional cardholder authentication prior to resubmitting the transaction.",
    "06": "Error",
    "07": "EFT Velocity parameter record is missing",
    "08": "Approved authorization, Honor with identification",
    "09": "Location Velocity limit has been exceeded",
    "10": "Group Velocity limit has been exceeded",
    "11": "Approved authorization, VIP Approval",
    "12": "Invalid transaction",
    "13": "Invalid amount",
    "14": "Invalid card number",
    "15": "Invalid Issuer",
    "16": "Account not active",
    "17": "Declined per cardholder request",
    "18": "Reversal failed due to transaction already was reversed, was not found, or did not require reversal (error, decline).",
    "19": "Re-enter transaction",
    "20": "A non-CRIN (inside) transaction has been found in the Velocity file",
    "21": "An unknown Velocity error has occurred",
    "23": "Exact duplicate batch detected on upload. Upload not allowed or required.",
    "24": "Batch upload error. Refer to Bit 48 tag ZZ and Bit 62 tag H2.",
    "28": "Declined. Bad authorization number.",
    "30": "Format error, invalid value in message",
    "32": "Duplicate reference number error",
    "33": "Expired card",
    "36": "Additional Cardholder Authentication Required Visa and American Express Only",
    "38": "Invalid PIN",
    "39": "An invalid PIN has been entered the maximum number of times.",
    "40": "Requested function not supported",
    "43": "Lost or stolen card",
    "51": "INSUFFICIENT FUND FOR EBT TRANSACTIONS",
    "54": "Invalid Expiry Date",
    "57": "Tran Not Allowed For Cardholder",
    "58": "Transaction not permitted to terminal",
    "61": "Exceeds withdrawal limits",
    "62": "Restricted Card",
    "63": "MAC not verified or Incorrect MAC",
    "64": "Sender details not provided",
    "65": "Activity count limit exceeded",
    "81": "Invalid PIN block or Security violation",
    "84": "Security Counter error",
    "85": "No keys",
    "86": "ZEK sync error",
    "87": "ZPK sync error",
    "88": "ZAK sync error",
    "91": "Issuer or switch operative",
    "92": "Unable to Determine Network Routing",
    "93": "Busy – Pls Retry",
    "96": "Encryption Error",
    "97": "System Error",
    "98": "Database Error",
    "99": "Unable to send transaction to be authorized by issuer."
}
    return responsecodes[code]

}

function formatXml(xml) {
    return xml.replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#39;");
}

function block(requestFormat, TransType, request, response, ResponseText, TransactionIdentifier, CardType, tt){

    if (requestFormat.toUpperCase() == "XML"){
          request = formatXml(request)
          response = formatXml(response)
    }
    var blockContent = `
            <p class="trn">${TransType}</p>
            <div id="owl-example" class="trndiv owl-carousel">
                <div class="item">
                    <div>
                        <a class="float-button" id=tt+'_button_req' data-toggle="tooltip" data-placement="bottom" title="Copy" onclick="copyToClipboard('#"+tt+"_request', '#"+tt+"_button_req')"><i class="fas fa-copy"></i></a>
                    </div>
                        <div><pre><code id=tt+"_request">${request}</code></pre></div>
                    </div>
                    <div class="item">
                        <div>
                            <a class="float-button" id='gcb_button_res' data-toggle="tooltip" data-placement="bottom" title="Copy" onclick="copyToClipboard('#gcb_response', '#gcb_button_res')"><i class="fas fa-copy"></i></a>
                        </div>
                        <div><pre><code id="gcb_response">${response}</code></pre></div>
                </div>
            </div>
            <div class="shadow-textarea w-100">
                <div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100  p-2" ><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-5" style="font-weight:600">Response Text :  ${ResponseText}</span></div>
            </div>
            <div class="shadow-textarea w-100">
                <div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100  p-2" ><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-5" style="font-weight:600">TransactionID :  ${TransactionIdentifier}</span></div>
            </div>
            <div class="shadow-textarea w-100">
                <div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100  p-2" ><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-5" style="font-weight:600">Card Type :  ${CardType}</span></div>
            </div>`;
        return blockContent
}


function getTransactionDetails(requestFormat, requestData, responseData, TransactionTypeCode, Transaction_Type) {
    let isCancelLast = TransactionTypeCode.includes("76");
    request = (!isCancelLast) ? requestData.TransRequest : requestData.CancelLastTransRequest;
    response = (!isCancelLast) ? responseData.TransResponse : responseData.CancelLastTransResponse;
    transactionData = (isCancelLast) ? transactionData = response : (requestFormat === "JSON") ? response?.TransDetailsData?.TransDetailData?.[0] ?? "" : response?.TransDetailsData?.TransDetailData ?? "";
    var transaction = {
        CardNumber: transactionData?.CardNumber ?? "",
        CIToken: transactionData?.CardIdentifier ?? "",
        CRMToken: transactionData?.CRMToken ?? "",
        CardEntryMode: transactionData?.CardEntryMode ?? "",
        TransactionTypeCode: transactionData?.TransactionTypeCode ?? "",
        TransactionSequenceNumber: transactionData?.TransactionSequenceNumber ?? "",
        CardType: transactionData?.CardType ?? "",
        SubCardType: transactionData?.SubCardType ?? "",
        RequestAmount: requestData?.TransAmountDetails?.TransactionTotal ?? "",
        TransactionAmount: transactionData?.TotalApprovedAmount ?? "",
        ResponseText: transactionData?.ResponseText ?? "",
        ResponseCode: transactionData?.ResponseCode ?? "",
        TransactionIdentifier: transactionData?.TransactionIdentifier ?? "",
        AurusPayTicketNum: responseData?.AurusPayTicketNum ?? "",
        ApprovalCode: transactionData?.ApprovalCode ?? "",
        ReceiptInfo: transactionData?.ReceiptDetails ? JSON.stringify(transactionData.ReceiptDetails, null, 4) : "",
        FleetPromptsData: transactionData?.FleetPromptsData ? JSON.stringify(transactionData.FleetPromptsData, null, 4) : "",
        responseTextColor : transactionData?.ResponseText === "APPROVAL" ? "green" : "red",
        identifierColor : transactionData?.TransactionIdentifier === 18 ? "green" : "red",
        Products: JSON.stringify(
            requestData?.Level3ProductsData ??
            requestData?.FleetData ??
            requestData?.EPPDetailsInfo ??
            "{}",
            null, 4
        )
    };
    var TransRow = `<tr>
            <td>${Transaction_Type}</td>
            <td>${transaction.CardEntryMode}</td>
            <td>${transaction.TransactionTypeCode}</td>
            <td>${transaction.CardType}</td>
            <td>${transaction.SubCardType}</td>
            <td>${transaction.RequestAmount}</td>
            <td>${transaction.TransactionAmount}</td>
            <td style="color: ${transaction.responseTextColor}">${transaction.ResponseText}</td>
            <td>${transaction.ResponseCode}</td>
            <td style="color: ${transaction.identifierColor}">${transaction.TransactionIdentifier}</td>
            <td>${transaction.AurusPayTicketNum}</td>
            <td>${transaction.ApprovalCode}</td>
        </tr>`;
    var Parent_owl_data = '<div id="owl_data' + transaction.TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB RESPONSE ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + transaction.ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + transaction.Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + transaction.FleetPromptsData + '</code></pre></div></div>'
    var Parent_data = $('<div class="card ' + transaction.responseTextColor + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + transaction.TransactionIdentifier + '"><a class="card-link"># ' + Transaction_Type  + transaction.TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + transaction.TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + Parent_owl_data + '</div></div></div>').hide();
    $("#accordion").append(Parent_data);
    $(Parent_data).fadeIn("slow");
    $("#owl_data" + transaction.TransactionIdentifier).owlCarousel({
        autoPlay: 3000,
        items: 1,
        margin: 10,
        itemsDesktop: [1199, 1],
        itemsDesktopSmall: [979, 1],
        navigation: false,
        responsiveClass: true,
        responsive: { 0: { items: 1, }, 600: { items: 1, }, 1000: { items: 1, } }
    });
    return $(TransRow).hide();
}


function Transaction_report(itr, data, Transaction_type, isSingle) {
    console.log(data)
    let gcbRow = null, parentRow = null, childRow = null, childOfChildRow = null, Gcb_Transaction_CardToken = null, rowspan = "0";
    let gcbBlock, parentBlock, childBlock, childOfChildBlock = null;
    var CARDNAME = null;
    let childTransactionType = Transaction_type.split("_");
    requestFormat = data.Data.RequestFormat
    GCBData = data.Report.GCB
    parentData = data.Report.Parent
    childData = data.Report.Child
    childOfChild = data.Report.ChildOfChild
    Parent_TransactionType = parentData.TransactionType
    Child_TransactionType = childData.TransactionType
    Child_of_Child_TransactionType = childOfChild.ChildofChildTransactionType
    GCB_request = data.Report.GCB.Request
	GCB_response = data.Report.GCB.Response
	parent_Request = parentData.Request
    Parent_Response = parentData.Response
    Child_Request =  childData.Request
    Child_Response = childData.Response
    Child_of_child_Transaction_request =  childOfChild.Request
    Child_of_child_Transaction_response = childOfChild.Response
    if(GCB_response != null) {
        rowspan = "2"
        GCB_UNKN = ""
        GCBRquest = GCB_request.GetCardBINRequest
        GCBResponse = GCB_response.GetCardBINResponse
        Gcb_Transaction_CIToken = GCBResponse?.ECOMMInfo?.CardIdentifier ?? "";
        Gcb_Transaction_CardToken = GCBResponse?.CardToken ?? "";
        Gcb_Transaction_CRMToken = GCBResponse?.CRMToken ?? "";
        Gcb_LookupFlag = GCBRquest?.LookUpFlag ?? "";
        Gcb_Transaction_CardEntryMode = GCBResponse?.CardEntryMode ?? "";
        Gcb_Transaction_CardType = GCBResponse?.CardType ?? "";
        Gcb_Transaction_SubCardType = GCBResponse?.SubCardType ?? "";
        Gcb_Transaction_ResponseText = GCBResponse?.ResponseText ?? "";
        Gcb_Transaction_ResponseCode = GCBResponse?.ResponseCode ?? "";
		Gcb_Transaction_NonFinancialToken = GCBResponse?.NonFinancialToken ?? "";
		CARDNAME =  GCBResponse?.FirstName ?? "";
        gcbRow = $('<tr><td>' + "GCB" + Gcb_LookupFlag +'</td><td>' + Gcb_Transaction_CardEntryMode + '</td><td>' + GCB_UNKN + '</td><td>' + Gcb_Transaction_CardType + '</td><td>' + Gcb_Transaction_SubCardType + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + Gcb_Transaction_ResponseText + '</td><td>' + Gcb_Transaction_ResponseCode + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td></tr>').hide();
        gcbBlock = block(requestFormat, "GCB", GCB_request, GCB_response, GCBData.ResponseText, GCBData.TransactionID, GCBData.CardType, "gcb")
   }
    if (Parent_TransactionType != null &&  Parent_Response != null) {
        rowspan = "3"
        parentRow = getTransactionDetails(requestFormat, parent_Request, Parent_Response, childTransactionType[0], Parent_TransactionType)
        parentBlock = block(requestFormat, Parent_TransactionType, parent_Request, Parent_Response, parentData.ResponseText, parentData.TransactionID, "", "parent")
    }
    if (Child_TransactionType != null && Child_Response != null){
        rowspan = "4"
        childRow = getTransactionDetails(requestFormat, Child_Request, Child_Response, childTransactionType[1], Child_TransactionType)
        childBlock = block(requestFormat, Child_TransactionType, Child_Request, Child_Response, childData.ResponseText, childData.TransactionID, "", "child")
    }
    if (Child_of_Child_TransactionType != null && Child_of_child_Transaction_response != null){
        rowspan = "5"
        TransData = getTransactionDetails(requestFormat, Child_of_child_Transaction_request, Child_of_child_Transaction_response, childTransactionType[2], ChildofChildTransactionType)
        childOfChildBlock = block(requestFormat, Child_of_Child_TransactionType, Child_of_child_Transaction_request, Child_of_child_Transaction_response, childOfChild.ResponseText, childOfChild.TransactionID, "", "childofchild")
    }
     if(isSingle == false){
            var first_row = $('<tr><td rowspan="' + rowspan + '">' + Gcb_Transaction_CardToken + ' | ' + Gcb_Transaction_NonFinancialToken +'</td><td rowspan="' + rowspan + '">' + CARDNAME + '</td></tr>').hide();
            if (gcbRow != null) { $("#divBody").append(first_row); $(first_row).fadeIn("slow"); $("#divBody").append(gcbRow); $(gcbRow).fadeIn("slow"); }
            if (parentRow != null) { $("#divBody").append(parentRow); $(parentRow).fadeIn("slow"); }
            if (childRow != null) { $("#divBody").append(childRow); $(childRow).fadeIn("slow"); }
            if (childOfChildRow != null) { $("#divBody").append(childOfChildRow); $(childOfChildRow).fadeIn("slow"); }
        }
       else{
            if(gcbBlock != null){ $("#TransactionBlock_gcb").append(gcbBlock); $(gcbBlock).fadeIn("slow"); }
            if(parentBlock != null){ $("#TransactionBlock_parent").append(parentBlock); $(parentBlock).fadeIn("slow"); }
            if(childBlock != null){ $("#TransactionBlock_child").append(childBlock); $(childBlock).fadeIn("slow"); }
            if(childOfChildBlock != null){ $("#TransactionBlock_childofchild").append(childOfChildBlock); $(childOfChildBlock).fadeIn("slow"); }
            $(".trndiv").owlCarousel({
                autoPlay: 3000,
                items: 3,
                margin: 10,
                itemsDesktop: [1199, 1],
                itemsDesktopSmall: [979, 1],
                navigation: true,
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,

                    },
                    600: {
                        items: 1,

                    },
                    1000: {
                        items: 1,
                    }
                }
            });
       }
  }

function finalizeUI() {
    $("#loader").remove();
    $('#itr').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#Transaction_Type').prop('disabled', false);
    $('#export_btn').removeClass('d-none');
    $('#message').html('<p class="text-center text-danger"><b>Iteration Completed</b></p>').fadeIn(1500);
}