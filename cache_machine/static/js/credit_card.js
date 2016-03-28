app.controller("EnterCardCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    $scope.input_label = 'Введите номер карты';
    $scope.enter_value = '';
    $scope.valid_number = false;
    $scope.press_key = function(num){
        if ($scope.enter_value.length < 16) {
            $scope.enter_value = $scope.enter_value + num;
            $scope.valid_number = $scope.enter_value.length == 16;
            if ($scope.enter_value.length < 5) {
                $scope.show_value = $scope.enter_value;
            } else {
                if ($scope.enter_value.length < 9) {
                    $scope.show_value = $scope.enter_value.replace(/(\d{4})(\d{0,4})/g, "$1-$2")
                } else {
                    if ($scope.enter_value.length < 13) {
                        $scope.show_value = $scope.enter_value.replace(/(\d{4})(\d{4})(\d{0,4})/g, "$1-$2-$3")
                    } else {
                        $scope.show_value = $scope.enter_value.replace(/(\d{4})(\d{4})(\d{4})(\d{0,4})/g, "$1-$2-$3-$4")
                    }
                }
            }
        }
    }
    $scope.send_card_number = function(){
        if ($scope.enter_value.length == 16) {
            Restangular.one('account_active', $scope.enter_value).get().then(function(resp){
                if (resp.active) {
                    user_card_number =  $scope.enter_value;
                    $location.path('/enter_pin');
                } else {
                    error_text = 'Карта заблокирована';
                    error_back_url = '/';
                    $location.path('/error');
                }
            }, function(response) {
                error_text = 'Карта не найдена';
                error_back_url = '/';
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
