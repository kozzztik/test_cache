app.controller("GetMoneyCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    if (!user_card_number) {
        $location.path('/');
    }
    $scope.input_label = 'Введите сумму';
    $scope.enter_value = '';
    $scope.valid_number = false;
    $scope.press_key = function(num){
        if ($scope.enter_value.length < 16) {
            if ((num != 0)|($scope.enter_value.length > 0)) {
                $scope.enter_value = $scope.enter_value + '' + num;
                $scope.valid_number = true;
                $scope.show_value = $scope.enter_value;
            }
        }
    }
    $scope.send_card_number = function(){
        if ($scope.enter_value.length > 0) {
            Restangular.one('get_money').customPOST({value: $scope.enter_value * 100}).then(function(resp){
                if (resp.success) {
                    user_card_number =  $scope.enter_value;
                    $location.path('/get_money_result');
                } else {
                    error_text = resp.reason;
                    error_back_url = '/get_money';
                    $location.path('/error');
                }
            }, function(response) {
                error_text = response;
                error_back_url = '/get_money';
                $location.path('/error');
            })
        }
    }
    $scope.clear_card_number = function(){
        $scope.enter_value='';
        $scope.show_value='';
        $scope.valid_number = false;
    }
}])
