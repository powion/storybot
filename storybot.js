try {
    var app = angular.module('myApp', []);

    app.controller('myCtrl', function($scope) {
        $scope.selectSource = function ($event, $source) {
            $scope.currentSource.hide = true;
            $scope.currentSource = $source;
            $scope.currentSource.hide = false;
            // highligt the currently selected tab
            tabitems = document.getElementsByClassName("tabitems");
            for (i = 0; i < tabitems.length; i++) {
                tabitems[i].className =
                        tabitems[i].className.replace(" w3-dark-grey", "");
            }
            $event.currentTarget.className += " w3-dark-grey";
        }

        $scope.sources = [
            {
                // PRIDE AND PREJUDICE -----------------------------------------
                name:"Pride and Prejudice",
                hide:true,
                text:
                  [
                  // pap text 1:
                  "i feel as he had probably be of age since , with and then added the room , i do like her brother appearance at his coming into anything was not for me to . we must have something more wrong to her the next imprudence had any partiality provoked her own family ! never seen saw anything extraordinary now to spend the day altogether a most man whose manners ! yes , she called in which happiness no obligation for it ? has he was as foolish enough things , and then they would not try if possible what , saying to do it . you ought , or the being an early age since the spring ! no , kitty kitty was the happy man on her , your goodness too . elizabeth then by her . he was very fond of of them all . thank god 's behaviour attentively , and that i am growing every other subject , was as regular much disposed to like him . it had not a letter temper . when she came into hertfordshire , who is it about the dance . i am sorry not ashamed of you for this was the surprise of it is not safe from the hope of revenging himself . , to whom she had believed lady catherine was still",
                  // pap text 2
                    "frodo was delighted with a wave of all that we make up good deal about them , and then we shall be able master , who are unused to find the world is changing now called accursed hills . but samwise , will you each each time , we can keep awake could make only for a guess at hand , and they felt the wind seemed in its choked path . he jumped up and went to out , wet sky . the grass , but in other the language of orthanc yet at last , to elvenhome that that he could deal with them . but who has studied heard something that would be a danger , as if thinking they had walked for the time comes of a great storm ship , wrought of living men were dead , so near that even the hobbits and strode forward , using the authority weapon . i will take neither strength of the elves , ? very mighty works of gondor that the company was arranged taking ."
                  ]
            },
            // TOLKIEN ---------------------------------------------------------
            {
                name:"Tolkien",
                hide:true,
                text:[
                  // tolkien text 1
                  "frodo was delighted with a wave of all that we make up good deal about them , and then we shall be able master , who are unused to find the world is changing now called accursed hills . but samwise , will you each each time , we can keep awake could make only for a guess at hand , and they felt the wind seemed in its choked path . he jumped up and went to out , wet sky . the grass , but in other the language of orthanc yet at last , to elvenhome that that he could deal with them . but who has studied heard something that would be a danger , as if thinking they had walked for the time comes of a great storm ship , wrought of living men were dead , so near that even the hobbits and strode forward , using the authority weapon . i will take neither strength of the elves , ? very mighty works of gondor that the company was arranged taking ."
                ]
            },
            // TIFU ------------------------------------------------------------
            {
                name:"Reddit: TIFU",
                hide:true,
                text:[
                  "hello again...."
                ]
            }
        ];

        $scope.currentSource = $scope.sources[0];
    });
} catch(e) {
    console.log(e);
}
