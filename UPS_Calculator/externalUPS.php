<?php header('Access-Control-Allow-Origin: *'); ?>

<?php 

    include_once 'ups.rate.class.php'; 
    include_once 'usps.php';

            function test_input($data){
                $data = trim($data);
                $data = stripslashes($data);
                $data = htmlspecialchars($data);
                return $data;
            }
        
            $objUpsRate = new UpsShippingQuote();

            //$strDestinationZip = test_input($_POST["varZip"]);
            $strDestinationZip = test_input($_GET["varZip"]);
            //$strMethodShortName = test_input($_POST["varShipping"]);
            $strMethodShortName = test_input($_GET["varShipping"]);

            // box dimensions from amy
            $strPackageLength = 12;
            $strPackageWidth = 10;
            $strPackageHeight = 3;

            // weight varies depending on type of swatch kit, have a median one hardcoded now
            $strPackageWeight = 11.5;
            $boolReturnPriceOnly = true;
            $strUSPSWeight = 5;
            $strUSPSZip = test_input($_POST["varZip"]);
            $strUSPSShip = test_input($_POST["USPSvarShipping"]);
            
            switch($strUSPSShip) {
                case 'O':
                    $USPSCode = "PRIORITY MAIL EXPRESS";
                    break;
                case 'P':
                    $USPSCode = "PRIORITY";
                    break;
                default;
                    $USPSCode = "PRIORITY";
                    break;  
            }

            switch($strMethodShortName) { 
            case '1DM':            
                $strServiceCode = "Next Day Air Early AM"; 
                break; 
            case '1DA':            
                $strServiceCode = "Next Day Air"; 
                break;          
            case '1DP':            
                $strServiceCode = "Next Day Air Saver"; 
                break; 
            case '2DM':            
                $strServiceCode = "Second Day Air AM"; 
                break; 
            case '2DA':            
                $strServiceCode = "Second Day Air"; 
                break; 
            case '3DS':            
                $strServiceCode = "Three Day Select"; 
                break; 
            case 'GND':            
                $strServiceCode = "Ground"; 
                break; 
            case 'STD':            
                $strServiceCode = "Standard"; 
                break; 
            case 'XPR':            
                $strServiceCode = "Worldwide Express"; 
                break; 
            case 'XDM':            
                $strServiceCode = "Worldwide Express Plus"; 
                break; 
            case 'XPD':            
                $strServiceCode = "Worldwide Expedited"; 
                break; 
            default:            
                $strServiceCode = "Ground"; 
                break; 
            }
            $result = $objUpsRate->GetShippingRate(
                $strDestinationZip, 
                $strMethodShortName, 
                $strPackageLength, 
                $strPackageWidth,
                $strPackageHeight, 
                $strPackageWeight, 
                $boolReturnPriceOnly
            );

            if ($result != '')
            {
                echo "$" . $result;
            }
            else 
            {
                echo "Please enter a valid zipcode";
            }

            

?>