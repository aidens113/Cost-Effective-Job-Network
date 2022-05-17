<?php
#########################################
#MYSQLI FUNCTIONS
#########################################
function getEmailByJobID($jobID){
    $mysqli = mysqli_connect("localhost", "censored", "censored", "censored");
    $result = mysqli_query($mysqli, "SELECT * FROM main WHERE jobid = '".$jobID."';");
    
    while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
    $email = strval($row["email"]);
    }
    $mysqli -> close();
    return $email;
}

function getSentByJobID($jobID){
    $mysqli = mysqli_connect("localhost", "censored", "censored", "censored");
    $result = mysqli_query($mysqli, "SELECT * FROM main WHERE jobid = '".$jobID."';");
    
    while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
    $sent = strval($row["sent"]);
    }
    $mysqli -> close();
    return $sent;
}

function insertNewJob($jobid,$email){
    $mysqli = mysqli_connect("localhost", "censored", "censored", "censored");
    $result = mysqli_query($mysqli, "INSERT INTO main (email,jobid,sent) VALUES ('".$email."','".$jobid."','0');");
    $mysqli -> close();
}

function insertSent($jobid,$newSent){
    $mysqli = mysqli_connect("localhost", "censored", "censored", "censored");
    $result = mysqli_query($mysqli, "UPDATE main SET sent = ".$newSent." WHERE jobid = '".$jobid."';");
    $mysqli -> close();
}

function deleteSQLJob($jobid){
    $mysqli = mysqli_connect("localhost", "censored", "censored", "censored");
    $result = mysqli_query($mysqli, "DELETE FROM main WHERE jobid = '".$jobid."';");
    $mysqli -> close();
}
#############################################
#BASIC FUNCTIONS
#############################################
function doEmail($to,$subject,$msg){
    $mailheader = "From: Aiden <admin@seo-tips.tech>\r\n";
    $mailheader .= "Reply-To: admin@seo-tips.tech\r\n";
    mail($to,$subject,$msg,$mailheader); 
}

function readThisFile($filename){
    $myfile = fopen($filename, "r") or die("Unable to open file!");
    $contents = fread($myfile, filesize($filename));
    fclose($myfile);
    return $contents;
}

function writeNewFile($filename, $stufftowrite){
    $myfile = fopen($filename, "w") or die("Unable to open file!");
    fwrite($myfile, $stufftowrite);
    fclose($myfile);
}

function appendToFile($filename, $stufftowrite){
    $myfile = fopen($filename, "a") or die("Unable to open file!");
    fwrite($myfile, $stufftowrite);
    fclose($myfile);
}

#####################################
#ADMIN COMMANDS
#####################################
function postJob($title,$html,$email){
    try{
        $directory = strval(dirname(__FILE__))."/directory/";
        $directorypending = strval(dirname(__FILE__))."/pending/";
        $thisID = count(scandir($directory));
        $FINALID = (intval($thisID)+1);
        $thisLink = "'https://projectmanager.seo-tips.tech/apply-to-job/?jobid=".$FINALID."'";
        $firstHTML = readThisFile("template.html"); 
        $finalHTML = str_replace("*JOB TITLE*",$title,$firstHTML);
        $finalHTML = str_replace("*THISHTML*",$html,$finalHTML);
        $finalHTML = str_replace("*SIGNUPURL*",$thisLink,$finalHTML);
        insertNewJob($FINALID,$email);
        writeNewFile(($directorypending."jobpost".strval($FINALID).".html"), $finalHTML);
        doEmail("alertemail","NEW JOB POST REQUEST",strval("There is a new job request. \n\rYou can find it here: https://yourdomain.com/mmbot/pending/jobpost".$FINALID.".html\n\rAccept it here: https://yourdomain.com/mmbot/moderation.php?cmd=acceptjob&jobid=".$FINALID."&passw=sdljfkljkl3j2kjkl23jfklj23kljfklj23kljklsdjfkldsjfklsdjf \n\rContact Email: ".$email));
        header("Location: https://projectmanager.seo-tips.tech/thanks/");
    }catch(Exception $e){
        echo 'Caught exception: ',  $e->getMessage(), "\n";
    }
}

function deletePendingJob($jobid){
    $directory = strval(dirname(__FILE__))."/pending/";
    $jobURL = ($directory."jobpost".strval($jobid).".html");
    unlink($jobURL); 
}
function deleteJob($jobid){
    $directory = strval(dirname(__FILE__))."/directory/";
    $jobURL = ($directory."jobpost".strval($jobid).".html");
    unlink($jobURL); 
    
    $directory = strval(dirname(__FILE__))."/coverletters/";
    $thisi = 0;
    while(true){
        $thisi = ($thisi + 1);
        $filethisname = strval("coverletter".$jobid."_".$thisi);
        $thisfile = strval($directory."coverletter".$jobid."_".$thisi.".html");
        if(file_exists($thisfile)){
            unlink($thisfile); 
        }
        else{
            break;
        }
    }
    deleteSQLJob($jobid);
}
function acceptJob($jobid){
    $directorypending = strval(dirname(__FILE__))."/pending/";
    $directory = strval(dirname(__FILE__))."/directory/";
    $jobURL = ($directorypending."jobpost".strval($jobid).".html");
    $newJobURL = ($directory."jobpost".strval($jobid).".html");
    $file = readThisFile($jobURL);
    writeNewFile($newJobURL,$file);
    deletePendingJob($jobid);

} 
function declineJob($jobid){
    deleteJob($jobid);
}

function acceptResume($applicationID,$jobID){
    $email = getEmailByJobID($jobID);
    $sentAmount = getSentByJobID($jobID);
    insertSent($jobID,strval(intval($sentAmount + 1)) );
    doEmail($email,"NEW APPLICATION SUBMITTED!",strval("Hello, A new application has been submitted on your job. You can view it here: https://projectmanager.seo-tips.tech/mmbot/coverletters/".$applicationID));
}

#CONSUMER COMMANDS
function applyToJob($jobid, $email, $coverletter, $linktoresume, $linktowebsites){
    $sentAmount = getSentByJobID($jobid);
    $directory = strval(dirname(__FILE__))."/coverletters/";
    $thisi = 0;
    while(true){
        $thisi = ($thisi + 1);
        $filethisname = strval("coverletter".$jobid."_".$thisi.".html");
        $thisfile = strval($directory."coverletter".$jobid."_".$thisi.".html");
        if(!file_exists($thisfile)){
            break;
        }
    }
    $templateFile = readThisFile("applicationTemplate.html");
    $application = str_replace("*THISHTML*",$coverletter,$templateFile);
    $application = str_replace("*EMAIL*",$email,$application);
    $application = str_replace("*RESUME*",$linktoresume,$application);
    $application = str_replace("*LINKS*",$linktowebsites,$application);
    writeNewFile($thisfile,$application); 
    
    $thisText = "STARTNEW APPLICATION \r\n";
    $thisText .= "JOB: https://projectmanager.seo-tips.tech/mmbot/directory/jobpost".$jobid.".html\r\n";
    $thisText .= "APPLICANT EMAIL: ".$email."\r\n";
    $thisText .= "COVER LETTER LINK: https://projectmanager.seo-tips.tech/mmbot/coverletters/".$filethisname."\r\n";
    $thisText .= "LINK TO RESUME: ".$linktoresume."\r\n";
    $thisText .= "LINK TO WEBSITES: ".$linktowebsites."\r\n";
    $thisText .= "----------------------\r\n";
    $thisText .= "ACCEPT RESUME: <https://yourdomain.com/mmbot/moderation.php?cmd=acceptResume&applicationID=".$filethisname."&jobid=".$jobid.">\r\n";
    $thisText .= "RESUMES SENT: ".$sentAmount."\r\n";
    $thisText .= "----------------------\r\n";
    $thisText .= "DELETE JOB POSTING: <https://yourdomain.com/mmbot/moderation.php?cmd=deletejob&passw=sdljfkljkl3j2kjkl23jfklj23kljfklj23kljklsdjfkldsjfklsdjf&jobid=".$jobid.">\r\n";
    $thisText .= "END";
    appendToFile("incomingApplications.txt",$thisText);
    header("Location: https://projectmanager.seo-tips.tech/thanks-for-applying/");
}
if($_SERVER['REQUEST_METHOD'] == "POST"){
    $cmd = $_POST['cmd'];
}
if($_SERVER['REQUEST_METHOD'] == "GET"){
    $cmd = $_GET['cmd'];    
}

if($cmd == "postjob"){
    postJob($_POST['title'],$_POST['html'],$_POST['email']);    
}
if($cmd == "deletejob"){
    if($_GET["passw"] == "sdljfkljkl3j2kjkl23jfklj23kljfklj23kljklsdjfkldsjfklsdjf"){
        deleteJob($_GET['jobid']);
    }
}
if($cmd == "acceptjob"){
    if($_GET["passw"] == "sdljfkljkl3j2kjkl23jfklj23kljfklj23kljklsdjfkldsjfklsdjf"){
        acceptJob($_GET['jobid']);
    }
        
}
if($cmd == "acceptResume"){
    acceptResume($_GET['applicationID'],$_GET['jobid']);
}
if($cmd == "applyjob"){
    applyToJob($_POST['jobid'],$_POST['email'],$_POST['coverletter'],$_POST['linktoresume'],$_POST['linktowebsites']);
}
if($cmd == "deleteOldApplications"){
    writeNewFile("incomingApplications.txt", "");
}
if($cmd == "deleteOldJobs"){
    writeNewFile("incomingJobs.txt", "");
}

?>