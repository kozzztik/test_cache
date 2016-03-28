app.controller("InputMoneyCountCtrl", ['$scope', 'Restangular', '$q', '$location', '$state',
function ($scope, Restangular, $q, $location, $state) {
    if (!user_card_number) {
        $location.path('/');
    }
    $scope.input_label = 'Введите сумму';
    $scope.enter_value = '';
    $scope.valid_number = false;
    $scope.show_exit = true;
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
            get_money_count = $scope.enter_value
            $state.go('get_money_result');
        }
    }
    $scope.clear_card_number = function(){
        $scope.enter_value='';
        $scope.show_value='';
        $scope.valid_number = false;
    }
}])
