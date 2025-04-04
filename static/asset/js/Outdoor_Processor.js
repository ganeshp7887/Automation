function before_data_send(i, message) {
    $('#loader').show();
    a = $('<div id="img">Icon</div><div id="desc">A notification message..</div>').hide();
    str = $('<div class="p-1"><div class="spinner-border text-white" role="status" style="vertical-align: middle;"></div><span class="text-center m-5"># ' + i +' '+message+'</span></div>').hide();
    $("#trans_progress").html(str);
    $(str).fadeIn(1000);
}

function finalizeUI() {
    $("#loader").remove();
    $('#itr').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#Transaction_Type').prop('disabled', false);
    $('#export_btn').removeClass('d-none');
    $('#message').html('<p class="text-center text-danger"><b>Iteration Completed</b></p>').fadeIn(1500);
}

function onSubmitClick(){
    var g = document.getElementById('Transaction_Type').validity.valid;
    var t = document.getElementById('cds').validity.valid;
    if (g == false || t == false){
        alert("data missing");
    }
    else{
        $('#cds').prop('disabled', true);
        $('#submit').prop('disabled', true);
        $('#Transaction_Type').prop('disabled', true);
        $('#gcb_type').prop('disabled', true);
        $('#OnPinkey').prop('disabled', true);
        $('#product_count').prop('disabled', true);
        table_header = $('<tr id="head1"><th>CardToken</th><th>Request</th><th>EntryMode</th><th>TransType</th><th>ExpectedCardType</th><th>ActualCardType</th><th>SubCardType</th><th>TrnsAmt</th><th>ApprovedAmt</th><th>ResponseText</th><th>ResponseCode</th><th>TransactionID</th><th>AurusPayTicketNum</th><th>ApprovalCode</th></tr>').hide();
        $("#table_header").html(table_header);
        $(table_header).fadeIn("slow");
        setTimeout(function() {
            readExcel();
        }, 500);
    }
   }

function updateMessage(message) {
    $('#message').html(`<p class="text-center align-items-center text-danger"><b>${message}</b></p>`);
}

function showLoaderMessage(message) {
    const loaderHtml = `
        <div class="w-100 text-center p-2" id="loader">
            <span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span>
            <span class="m-3">${message}</span>
        </div>`;
    $("#trans_progress").html(loaderHtml).hide().fadeIn(1500);
}

function switchBtn() {
    $(".panel-wrap").toggleClass("panel-unwrap");
    $(".sidepanel").toggleClass("sidepanel-unwrap");
    icon = $(this).find("i");
    if (icon.hasClass("fa-plus")){
        icon.addClass("fa-minus").removeClass("fa-plus");
      }else{
        icon.addClass("fa-plus").removeClass("fa-minus");
      }
}

function after_data_receive(data){
    if (data[0]["Error_count"] == "1") {
            $('#submit').prop('disabled', false);
            $('#cds').prop('disabled', false);
            $('#Transaction_Type').prop('disabled', false);
            $('#gcb_type').prop('disabled', false);
            $("#OnPinkey").prop('disabled', false);
			$('#product_count').prop('disabled', false);
            $('#trans_progress').hide();
            $("#table_header").hide();
			
         } else {
            str = $('<div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100 text-center p-2" id="loader"><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-3">Transaction completed</span></div>').hide();
           $("#trans_progress").html(str);
           $(str).fadeIn(1500);
            setTimeout(function() {
               $("#loader").remove();
               $('#submit').prop('disabled', false);
               $('#cds').prop('disabled', false);
               $('#Transaction_Type').prop('disabled', false);
               $('#gcb_type').prop('disabled', false);
               $("#OnPinkey").prop('disabled', false);
			   $('#product_count').prop('disabled', false);
               $('#export_btn').removeClass('d-none');
               $("#ErrorDiv").html("")
            }, 2000);
         }
}

function exportToExcel() {
   let table = document.getElementsByTagName("table"); // you can use document.getElementById('tableId') as well by providing id to the table tag
   let currentDate = new Date();
   var today = currentDate.toISOString().slice(0, 10);
   var time = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
   today.replace("-", "");
   time.replace("_", "");
   TableToExcel.convert(table[0], { // html code may contain multiple tables so here we are refering to 1st table tag
      name: 'Outdoor_testing_'+today+'_'+time+'.xlsx', // fileName you could use any name
      sheet: {
         name: 'Testing_Result' // sheetName
      }
   });
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
            <td></td>
            <td>${transaction.CardType}</td>
            <td>${transaction.SubCardType}</td>
            <td>${transaction.RequestAmount}</td>
            <td>${transaction.TransactionAmount}</td>
            <td style="color: ${transaction.responseTextColor}">${transaction.ResponseText}</td>
            <td>${transaction.ResponseCode}</td>
            <td>${transaction.TransactionIdentifier}</td>
            <td>${transaction.AurusPayTicketNum}</td>
            <td>${transaction.ApprovalCode}</td>
        </tr>`;
    var OwlData = '<div id="owl_data' + transaction.TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB RESPONSE ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + transaction.ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + transaction.Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + transaction.FleetPromptsData + '</code></pre></div></div>'
    var CollapseData = $('<div class="card ' + transaction.responseTextColor + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + transaction.TransactionIdentifier + '"><a class="card-link"># ' + Transaction_Type  + transaction.TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + transaction.TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + OwlData + '</div></div></div>').hide();
    $("#accordion").append(CollapseData);
    $(CollapseData).fadeIn("slow");
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

function Transaction_report(response, Transaction_type, iteration, isSingle) {
    let gcbRow, parentRow, childRow, childOfChildRow, Gcb_Transaction_CardToken  = null
    let rowspan = "0";
    let gcbBlock, parentBlock, childBlock, childOfChildBlock = null
    let childTransactionType = Transaction_type.split("_");
    if(response.Data.ErrorText != ""){
        $("#Error").html('<p class="red"><b>'+response.Data.ErrorText+'</p></b>')
    }
    requestFormat = response.Data.RequestFormat
    GCBData = response.Report.GCB
    parentData = response.Report.Parent
    childData = response.Report.Child 
    ChildOfChild = response.Report.ChildOfChild
    Parent_TransactionType = parentData.TransactionType
    Child_TransactionType = childData.TransactionType
    Child_of_Child_TransactionType = ChildOfChild.TransactionType
    Gcb_TransactionType = GCBData.TransactionType
    TrackData = response.Data.TrackData.replace("%B", "").split('^')[0];
    Parent_Transaction_CardNumber = TrackData;
    ExpectedCardType = response?.Data?.Expectedcardtype ?? "";
    GCB_request = GCBData.Request
    GCB_response = GCBData.Response
    parentRequest = parentData.Request
    ParentResponse = parentData.Response
    ChildRequest = childData.Request
    ChildResponse = childData.Response
    Child_of_child_Transaction_request = ChildOfChild.Request
    Child_of_child_Transaction_response = ChildOfChild.Response
    if(GCB_response != null) {
        rowspan = "2"
        GCB_UNKN = ""
        var GCB_request_data = GCB_request.GetCardBINRequest
        var GCB_response_data = GCB_response.GetCardBINResponse
        Gcb_fleet_prompts = GCB_response_data?.FleetPromptsFlag ?? "";
        Gcb_Transaction_CIToken = GCB_response_data?.ECOMMInfo?.CardIdentifier ?? "";
        Gcb_Transaction_CardToken = GCB_response_data?.CardToken ?? "";
        Gcb_Transaction_CRMToken = GCB_response_data?.CRMToken ?? "";
        Gcb_Transaction_CardEntryMode = GCB_response_data?.CardEntryMode ?? "";
        Gcb_Transaction_CardType = GCB_response_data?.CardType ?? "";
        Gcb_Transaction_SubCardType = GCB_response_data?.SubCardType ?? "";
        Gcb_Transaction_ResponseText = GCB_response_data?.ResponseText ?? "";
        Gcb_Transaction_ResponseCode = GCB_response_data?.ResponseCode ?? "";
        Gcb_Transaction_TransactionID = GCB_response_data?.TransactionIdentifier ?? "";
        const GCBResponseTextcolor = Gcb_Transaction_ResponseText === "Approved" ? "green" : "red";
        gcbRow = $('<tr><td>' + "GCB" + '</td><td>' + Gcb_Transaction_CardEntryMode + '</td><td>' + GCB_UNKN + '</td><td>' + ExpectedCardType + '</td><td>' + Gcb_Transaction_CardType + '</td><td>' + Gcb_Transaction_SubCardType + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + Gcb_Transaction_ResponseText + '</td><td>' + Gcb_Transaction_ResponseCode + '</td><td>' + Gcb_Transaction_TransactionID + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td></tr>').hide();
        var gcb_owl_data = '<div id="gcb_owl_data' + iteration + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB Request ' + '</p><hr><pre><code>' + JSON.stringify(GCB_request_data, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' GCB Response ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response_data, null, 4) + '</code></pre></div></div>'
        var gcb_data = $('<div class="card ' + GCBResponseTextcolor + '"><div class="card-header" data-toggle="collapse" href="#collapseGCB_' + iteration + '"><a class="card-link"># ' + "GCB" + ' Transaction ' + iteration + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapseGCB_' + iteration + '" class="collapse" data-parent="#accordion"><div class="card-body">' + gcb_owl_data + '</div></div></div>').hide();
        gcbBlock = block(requestFormat, "GCB", GCB_request, GCB_response, GCBData.ResponseText, GCBData.TransactionID, GCBData.CardType, "gcb")
    }
    if (Parent_TransactionType != null && ParentResponse != null) {
        rowspan = "3"
        parentRow = getTransactionDetails(requestFormat, parentRequest, ParentResponse, childTransactionType[0], Parent_TransactionType)
        parentBlock = block(requestFormat, Parent_TransactionType, parentRequest, ParentResponse, parentData.ResponseText, parentData.TransactionID, "", "parent")
    }
    if (Child_TransactionType != null && ChildResponse != undefined) {
        rowspan = "4"
        childRow = getTransactionDetails(requestFormat, ChildRequest, ChildResponse, childTransactionType[1], Child_TransactionType)
        childBlock = block(requestFormat, Child_TransactionType, ChildRequest, ChildResponse, childData.ResponseText, childData.TransactionID, "", "child")
    }
    if (Child_of_Child_TransactionType != null && Child_of_child_Transaction_response != null){
        rowspan = "5"
        childOfChildRow = getTransactionDetails(requestFormat, Child_of_child_Transaction_request, Child_of_child_Transaction_response, childTransactionType[2], Child_of_Child_TransactionType)
        childOfChildBlock = block(requestFormat, Child_of_Child_TransactionType, Child_of_child_Transaction_request, Child_of_child_Transaction_response, ChildOfChild.ResponseText, ChildOfChild.TransactionID, "", "childofchild")
    }
    if(isSingle == false){
        var first_row = $('<tr><td rowspan="' + rowspan + '">' + Parent_Transaction_CardNumber + '</td></tr>').hide();
        if (gcbRow != null) { $("#divBody").append(first_row); $(first_row).fadeIn("slow"); $("#divBody").append(gcbRow); $(gcbRow).fadeIn("slow"); }
        if (parentRow != null) { $("#divBody").append(parentRow); $(parentRow).fadeIn("slow"); }
        if (childRow != null) { $("#divBody").append(childRow); $(childRow).fadeIn("slow"); }
        if (childOfChildRow != null) { $("#divBody").append(childOfChildRow); $(childOfChildRow).fadeIn("slow"); }
    } else{
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