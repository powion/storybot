try {
    var app = angular.module('myApp', []);

    app.controller('myCtrl', function($scope) {

        // Change stories based on source selected
        // Called when tab items are clicked
        $scope.selectSource = function ($event, $source) {
            $scope.currentSource.hide = true;
            $scope.currentSource = $source;
            $scope.currentSource.hide = false;
            // highligt the currently selected tab
            tabitems = document.getElementsByClassName("tabitems");
            for (i = 0; i < tabitems.length; i++) {
                tabitems[i].className = tabitems[i].className
                    .replace(" w3-dark-grey", "");
            }
            $event.currentTarget.className += " w3-dark-grey";
            $scope.selectText(0);
        };

        $scope.currentTextIndex = 0;
        $scope.selectNextText = function () {
            $scope.currentTextIndex += 1;
            $scope.selectText($scope.currentTextIndex);
        }

        $scope.selectPrevText = function () {
            $scope.currentTextIndex -= 1;
            $scope.selectText($scope.currentTextIndex);
        }

        // Select a specific text from the current source
        $scope.selectText = function ($index) {
            texts = document.getElementsByClassName(
                $scope.currentSource.name + "-texts"
            );

            if ($index >= texts.length) {
                $index = 0;
            } else if ($index < 0) {
                $index = texts.length - 1;
            }

            for (i = 0; i < texts.length; i++) {
                texts[i].style.display = "none";
            }

            texts[$index].style.display = "block";
            $scope.currentTextIndex = $index;
        };

        $scope.sources = [
            // TIFU ------------------------------------------------------------
            {
                name:"/r/tifu",
                hide:true,
                text:[
                  "After a moment he ran out of the bathroom and started screaming in the lobby. The seat was up so I tried to take a quick deep breath so I couldn't imagine what else it could be fixed. She tells me she is done dating. I don't think I've ever cried with laughter. I find the guy fawkes skeleton conversation on the floor of the deck and watch something. I said no she's way out of my league she said then how are you dating me and tells me it is time to wait. Me being the mean. She tried to get to the porch and I are still together. We are trying to fix things our way back from school to an empty house so I decided. A few people started watching me and the security guard that she had an assignment. ",

                  "It's enough to wake up at 10 but have been together for 4 years ago was the only one. Get you manager. By the time I get up and walk around take a 10 or even 30 rarely minute break no problem. Obviously don't think I'm going to give him a fake name. One day in primary excitement. Also to the people saying that the were covered in feces. I went onto the balcony of the motel seeping. So the lady on the other side of the door and my legs were wide apart. The last I heard one was really fucking pissed at me and I go to the gate. She came in I spotted michael. ",

                  "In a space of a minute we hid all of the evidence. The alcohol the cigarettes dilation might be more expensive to. And for those interested I got 44. I am thinking this could possibly explain why I had so much. To answer some questions about their mommy. How. We find out through a mutual friend that this girl thinks chris is cute but still. Edit 2 : we never left the area of my work. I am in no way making fun if people with special needs. This is common. ",

                  "He gave me a look and see if you won $ 5,000 he didn't realize I had unwittingly. I am going to do if I see him again. **tl dr was completely naked with my dick in a glass. I thought that was it. I had to have a meeting with a smile on my face and puke all over his head and ripping inches. Instead of using my work computer I used my personal computer but can add me by using my name. So I recieved a new watch a few days ago I read a lot about it. What I am going to order some pizza and play some. You know who you are. I do not live on campus for a few hours and return with plans offend silly. ",

                  "... but what do you mean. Did I do to do wrong feeling like I've hurt her. I think she knows she screwed up and wo fingers but I'm kind of on the shy side of the road. I'm calling the police but I'm worried her son would respond and not do a thing about it. We sit down and start talking and he tells me that my id is obviously fake and that I did. But at the time I thought it would be fun to change the world. In 18 years we've never had a romantic history as we've always just seen one. While this is not a fucking lot too. Not long after my girlfriend. She wants to hang out on thursday. ",

                  "Today I'll pull over and give him the correct bag and explain I meant to say was would you prefer to work on my break this morning and my roommate made a new home. I wish I never started it. The absolute second I finish my sentence the word. After a moment he ran out of the office the effect of the one-way surgical. In one night I got drunk and started pushing her around and I not paying attention to my footing flags. Then they called us over from the gas station we swung. It was kinda like that but no matter. I told them to wait until they finish their speech and get to bed. On my first day because we sometimes crush on the same girls. I am a guy not a girl. ",

                  "Today I was in my late teens teachers were not amused at his response : I'm a programmer ship. And that is how I fucked up today. I really hope that you all will understand. I wo. So I went back to my house as we're driving I mention to him I'm thinkin mom and I'm not interested in looking around the office because it is similar to. We know each other and I have no idea I'm not a success either my sister or me. She's 45 minutes ago and I may be in the passenger seat. I didn't know whether to laugh or to cry. I tried to forget. I step into my father's right. ",

                  "Today I'm walking into the grocery prank my stepdad. It's become a point of contention. So I decided to tell my whole family the story. This will be a walk in the park compared attention. Tl dr : asked a guy to show me this in a comment on askreddit but I think it was 2 years accidental first guy I have her all wound up I slip off her dress. My dad works in the city and has a key to the apartment. I say no no just tell my mother. In the end I settled. Rip inbox : thanks anonymous. This was not surprising logged. ",

                    "Today I'm doing my best to reply to most if not all of the comments and will try to update when something happens. While site seeing during our trip to pound town. Anyway she called. Yep. I'm a single dude so I figured he would see the condom. If it's not next to water. Only it wasn't a sexual fantasy. Everything was going fine ... until he could give me food and invite me over. I walk to her seat at the. Head was standing in the bedroom when you get back you'll be fat again for a quick laugh and turn up the volume. ",

                    "And he's apologizing. I'm yelling at her that I'm fine just go I'm fine with it on my neck after that but I can say that I'd use a peanutmill workers. Rip my underwear off and the big one and has a jacuzzi sim. Due shouting at me in horror no. It's fine now but I started making double sure we had an afternoon appointment and talked through the local skating power. Through the sheets and into the mattress was soaked in the situation and even though they sympathized over and they all saw me. So here's the fu. So I start trying to yank any of the steak and continued to. I know I'm a 17 year old guy currently in high school but last friday I asked a girl classmate explode toy since haha : and it wasn't a dream ... I tell her I'd never been before and drinking. "
                ]
            },
            // tales from retail ------------------------------------------------------------
            {
                name:"/r/TalesFromRetail",
                hide:true,
                text:[
                  "I will call the woman w. I already know that i’m cheaper than anyone else and 20 % is a good about half my bill. His voice cracked and his son started crying. I don't think much of it at the time and was experienced in dealing frames. Me : yes I'm trying to find it. Next I check the counter in the morning would have to be certified. My husband was polite asked her how she would handle a customer making remarks gauge. I hand it to him and he says. Me : it's really honestly not a big deal. ",

                  "He suddenly lost all his drive through all he is done and the red woman was escorted out of the building one officer. She probably saw me. Edit : oh the upvotes. This is my money I found it. She's saying this as she was leaving the bathroom. I don't want to buy it then you need to pay for six and get another one from a customer when you pointed a gun at one of my employees. The guy wasn't moving in the new store manager. As I'm walking down the aisle with just a small printer in his cart that he didn't pay for because we didn't sell any clothing. Now get the hell out of the store. My other co-worker was out to lunch so I received no back up. ",

                  "She finally leaves I'm shaking. The other girl. It seemed too good to drink. C : fuck you then I'll just find someone who doesn't have access. My teller mix. I am not sitting here for a while and decided that I'm going to come back here again you. I work in a mobile phone shop in the mall going to night classes at college to be a good experience for her. This sweet guy bought his girlfriend a cute little gift bag from bath. A few days later telling him what we got her. So in this tale I. ",

                  "A technician wanted the cute girls light. The next morning I had the opening. My old friend qb asserts. We really didn't carry what she was saying or correct. I'll just get the girl to return this guy came up to cash a. Of course old dude asked to speak to the owner of the store. He walks away. Turning around to leave the store at once and I don't like it when you make my job harder. I don't even drive you. Good day and she tells me she will handle it. ",

                  "I was on the phone when this a 2 1/2 year old comes in. This customer is a guy whom walks over to me like that. I'm going to give me some monies. I swipe her way towards me every time I look up and the other girl on the registers and I can see her card thinking maybe she's just written it wrong but how kids say words wrong sometimes. The next week but I always forgot so my boss wouldn't like it if someone just dropped it in front of me. With a line of about ten people behind him. His efforts. I try to explain to her what happened but I'm really really sick and I'm so sorry for her. And she just let it go this once. The man had the most amazing and biggest.",

                  "Okay. This is now harder nor a more but you get along extra. He informed the customer just to double check and he had in his cart then walked back out and handed it to me. We start talking about and now there is nothing that we can do for you. Et : ugh. Well you're not doing anything*. But I'm just not comfortable using my own private credit card like this. I mean you could also give me 30€ a huge grin is wider over it and a hole. Better ask your mom in two weeks. Yl : like I mean like now. ",

                  "Now here's the good part. Using his receipt. I can tell that she is a very nice woman and everyone in the kitchen to make it. I don't know why along with him. He's not a big deal. This actually happens. In the last hour of my shift I'm just going to post this. B : now why do you need to know about our town. One day my boss asked if I would step in for a night or two. During these times I ever opened my store by myself all night. ",

                  "It's all my time at the bank. A couple of minutes but the other customers were doing we wouldn’t bigger on a puppy mind this is the same as a customer. I'll tell the manager about this - he and I are very good friends with a smile on my face because he took the money and took out his wallet and shows it to me and I total everything. He brings her to the emergency room. She starts ranting immediately about how horrible we all are for caring school and a couple of new jobs. I get up front just as they are walking into the store he saw the kid. I don't work here but they're probably familiar until he got there in fifteen minutes flat. And you know what I'm talking about right. Me : yes ma'am how is your visit. We get an email not long. ",

                  "Today I had a guy think. I 'm a decorator. Finally she says that her grandson is 9 in total for one person to let her see the cop. Again we are closed. We've spent over an hour with her at this point and we had never had a problem with that. In fact the reason she didn't do anything it just sat there. He gives me a short and rude no. Okay. I still input. A rational closer treatment routine. ",

                  "Me : ... looking. The mom is dying of laughter. He never came back saying he did but the call wasn't picked up. I tell her no unfortunately its against the rules. This woman had the patience of a different color. She expected that we would associate her 16 year old with her - and he turns away. I return with the box and after giving it a once over he buys a lot of stuff. I get there at 7:05. The kid went home. I asked my manager about it and learned the story : I'm here but this happened yesterday and I felt like a million bucks. ",
                ]
            },
            {
                name:"/r/talesfromtechsupport",
                hide:true,
                text:[
                    "Please leave and get on the network. I come in one morning and 7 people were around the office. I couldn’t see the ghost in the computer room to fix my computer needs that. I mumbled to myself as I collected all my belongings maybe it would all work out. Soon after we noticed he started sometimes coming in on days he wasn't scheduled to work and I have him email me the logs and I'll be right down to help him. If he hadn't been so lazy. They handle all alerts 3 : no it is sev. Me : can you send me a screenshot of the error occurred. It started out as a typical day I started I found out from some co-workers that the branch was known. He also had the next day off but what could the harm be.",

                        "Me : no. The conversation got ta go. Now type in : it allows me to script mouse. Last week's notice that another drive was being encrypted on top of the box was an ibm. Me : what the hell is this. He was a little shocked I was willing. I pressed the wrong option on the phone because I ca cnc document standard. That seemed to get things sorted itself is usually a high-end. We're distracted appropriately. Thanks again for that. ",

                        "Never heard of such a thing. What person needs $ 1200 of credit the only catch was getting business cards from his house. I went out and got another job and just decided to cut the coax. And was told that the only port for this on his laptop. I think back to the last couple of times I was holding. I got up from my chair staring at me. The user made an excuse. I tried to think of it. I've never used that. The head builder started smiling. ",

                        "I thought that was a good idea. Everyone was cold as shit lately. Mom : don't take me wrong something needs to be pre-approved. Few years ago I had a guy on hold for fifteen or twenty minutes. Then I will be on the phone when it happened the owner asked him to check anything. Plus this was a bit of a mystery ... I kid you not ... owner : no that will be all for today we will. This is it. Her mouth opened to retort. If it happens often we'll get to the computer and he calls me back after half an hour. * oh I'm sorry but I ca seem like I said I have to. ",

                        "I would help him as he kept telling me how noise on the firewall. I run a file type report to include. The vp was nodding. One hand however had again shot. It was redcheer who turned off my laptop. Can I have a nice day. After that she looked at me as if on queue we are the only providers of the service in this country who will roll that back no matter. Shortly after that my boss sits on the other side of the screen if it was in fact a special character that had defaulted millions. Me : maybe I should take a day or two and I would like to say something like so you need to open ports on the firewall before we can move any data from the backup and it's a half mile. She's pulled this kind of trouble. ",

                        "Me and her have the same model. Nice : for the hundredth practices transfer it to me to cut this idea down. But it wasn’t instant so the bloody hell is going on with the porting I'm going to speak up. It was a fine. Bhit had finally finished the account here I can see the door. We also had no sales staff other than rom and the amazon filling in and were short two technicians. Felonious. Avoid using the same password. He just got off the phone. As usual I ended up on work so I decided to log into their system and have a good day. ",

                        "I'll tell them I'm magic. He comes back a few hours later one of the staff called me. I handed him the gear and it's always really hot to the touch and it's working. My friend asked her why she got such a big server and apparently she thought that I'd hate to owe them money. Not because they're there to filter the insanity enters. I guess I'll call you later. As the door to her work our brief moment of temporary friendship work the next day this time around and gave the vp the biggest smile. Me : this is a vm. Me : then just minutes. Tl remoting'i 'm just trying to ruin her life. ",

                        "These are the best. The vp smiled away as he slowly tried to push the parts together every slight. I took a sip of my coffee before leaving the office. Head of hr looked at me. He was wearing dark. I tell him I'm going to need a new mouse. It came with and installed steam. I try to access it and you told me saying that her monitor has gone weird. It turned 90 degrees. I documented. ",

                        "Another hour and a half recovering indeed open my mouth and defend cd’s. It took me 3 months to finish a single month's data and the other pc drives as well. Guy shows up 15 minutes later with a huge box filled with paper on the desk picked up my coffee cup and left the building. **me : ** ok that shouldn't be down. Me : police had done my computer. I opened up the drive and my computers not just the one I am working on. There's two other computers in the room - didn't have the data to figure it out yet. Just. Wow it went that well then ask them for work. Nobody really said anything at first. ",

                        "I can find a small network switch. The two network cables and an extension cord and ... pt6 sets down and check all of the software. I will update if it was really him. Me : ok and right below that it should change but the process of getting the system to fire up. The managers were to ask you about his wife and football and everything under the sun with two isdn tiles will never support my name is bytewave how may I help you today. Customer : so it isn't technically a bare cat. He laughs lack waiting for the entire phone. I looked over to see angie. Morale statement ended with “i am authorized to answer any questions at this point. The entire it department was in a position to take it if their shift is about to end and it was on our official. "
                ]
            },
            {
                name:"/r/pettyrevenge",
                hide:true,
                text:[
                    "Edit : here's a picture of a woman having a bad day or whatever. Super petty revenge. Whenever the smokers would go on their cigarette breaks we would stop working the rest of the stuff. My daughter was collecting figure it out. She has some galaxy returning jess was also planning on giving it to the manager anyway. He spends interior. I pointed to the man in the head and the last straw was when she called me at home and started swearing at me. She called me a stupid bitch a few times until one day she screamed at my younger sister. Her seat was empty besides mine. This taxi completely full of groceries from all walks of her coming in to write said note and so on the day she was down and depressed sticks. ",

                    "The police there's a bunch. Since it was the best. He has long had a horrid very easy right next to me. I had seen the whole incident walked over and explained that he set them up and they are interrupting screaming. No. Well I do not want free samples given to the 3 apprentices. Ok I can do that. Except when I went into an empty gift card. The mc sends him to tell her to get a bit red in the face and says. Ok ... I'll do my best to help them. ",

                    "Normally a pretty immature kiosk. Until I heard why is she likes to be clean it's my car I say yes yes that sounds like a hell of a good idea to bring any kids at all. However i told them what you do and how many times. When the dad came up to the desk when the number. You did. The next morning he leaves and I go about my day the initial incident took place i was the acting supervisor who reports. He returns around 6:30 meanwhile the line. The right car decided he didn't want me to park in that spot. The guy behind me in line said they only have the two xbox's left for lunch a couple times. I pick it up and plan to throw it on her doorstep. ",

                    "Not only did he know something I didn't have 50 cents. As I get closer I notice two driver's licenses case and I found all the coupons he will find you. ** ok this just happened. So at my work we have a desk with two computers on each side so that the two long rows bucket amy's birthday and they needed someone to cover her. ** edit : just to clarify a few things I found. I called out for her twice and joked thank you very much from them us saying have a nice day and we left to go. It's like a one woman. She came over to our group and expecting a baby. So I work at the same place and having two other officers. Pick up the cash make change. ",

                    "So for the last 3 weeks at least 3 times a day to inform us he's having some work done on my friend should thank you. I hung up on my manager while she was still talking saying she would just pay for it. * he wouldn't allow me to personally put it in the bathroom and at the point of no return so I walked out and hit the light. He looks over at me and sees I start to ask a few probing boars. I turned around and said I think it's a priority. Since. Edit : I a word. Edit 2 : here is the picture I took of his daughter. This volleyball ball ever came over to the computer where they input showings. Edit : holy shit this blew seemed perfect. ",

                    "The third guy in line looked pissed but I explained that I had it. The meth ticked finally came to closing the account at the end of the year I decided I was tired of it. Next time there was a man and I will meet up to my end of the final year of my. I bought a $ 10 bill. I hand him the child's ticket along with his change - a bag of chew for that and I'm not a bridesmaid bsil ca theyre retail and let me say it. We called the owner and told him he needed to come in right now because we needed him and his friends. My main beef aid tonight was my birthday meal and as she turned to walk away my mother very quickly and carefully took the other day and they were both gone. I. Not certain. Anyway I rock eating and drinking for a few months.",

                    "I have always been nothing. She stuck on the front wall of the cart into a tree and put a huge smile was on. Every time the bus came to our stop after that I could not pass up and I were out to lunch. This also meant that she was lying - so despite having done no subway material. She ca glad to see you. : * oh you can go into the bathroom. She has only slipped up once when she must have pressed print the same time her phone rang I was passing the printer noticed the reams. So I did the opposite direction. I used to just leave a note that said we pay for this spot. No such luck bitch if you don't want to fight him. ",

                    "Luckily we have a small stereo included and I said yes. I would have talked to every person bob knew and the calls would have to stop at the next bus stop for no reason making this otherwise miserable. I hooked coffee and I tend light up after myself. So anyway I improvised 20s. I'm sorry. I'm a really patient person. I don't remember exactly the breakdown simply doesn't listen to me or do the work. This one time she came home from a casual date a real douchebag. He started the van turned around put stuff in the back of the store and my coworker is already there's no way. I remained calm and said normally I would but now I'm pissed off and threatened. ",

                    "My parents were already down there and took a taxi to get there. This lady had a mental breakdown even though you get a guy was more than a little uncomfortable especially since they liked to. He shoves girls even lesbians about it she was pissed. My mother. She has some extra curricular work here's where the sun comes out - and the lids dressed in a suit that fit him just a little too long finally. So I've made my way to work some guy cut off the car and turned it on and walked away. Fast forward a few months at that point was that he was cocky worth $ 20s. I'm sorry. I think I've done that has brought me joy. Alright I can deal and come in and use our electricity not pay rent etc. ",

                    "I called one up and he was male. Explained the situation she was. He flew all the way to the front where the coin agreement. She got off the bus a couple stops after that and I'm staring part of the night. Normally I'm the kind of guy who must have been a slow shift and my manager told me it may have been an over the top and go to pay for my copy. It was double sided so I thought it was funny albeit. Instead of taking the train set off again. The end of the world for her but I'm patient about it. I was so happy to hear it again. **tl customer couldn't help but laugh hysterically. "
                ]
            },
            {
                name:"/r/prorevenge",
                hide:true,
                text:[
                    "Well this guy and his brothers had had enough of him. The next week we were going to put them into school the next morning and got one with several replacement. I was walking down the hall and heard a large group of people and turns out melon decided to have a talk about john so I decided to go through this shit again I will set you on fire. No we didn't even work that night and I always id people. Don't they ever figured it was just. So I ate all of the box. It's about how I put a lot of money on tuition and I remember in my first meeting. Finally feeling tired lump and him and him douchebro turned red and walked out and we never saw him again either. I like to think that I was the one who the singer was with. She's an english professor who had a very shallow law.",

                    "And now it isn't exactly relevant. I had to choose a rumour printed right next to the barracks room by room dumping the contents of everyone's lockers to put our sketchbooks. She sent a picture of the ad he had to do to get the people involved. I contacted all the local news agencies to see who would do a block the # ... I've always been straight in the eye and said I don't really want to say that I am a member of a close friend. This friend who I'll call lovely. Lovely. Lovely was a year ago. He's big and dumb. They've been together for over a year so I took my sweet ass time with getting back she was hungover. Fuck that.",

                    "I am not helping you. Just as we get him all settled in court. My dad turns around and finally confesses such a perfect. A replacement card cost 40 $ 800. I stop myself. 'do af want to get caught. So. The beginning of june we started moving on to say that rather than outside pissing on his arm. The stupid pencil is lost. This was devastating as it began to show.",

                    "I gave her my information. She started harassing his family's phone and call the ez yet. He then requested that his order be to go off. I didn't submit a single one of my brothers. He got detention esme. I didn't bother me. My buddy is already pulling out his phone out from his desk and started our plan was to get into her email. He was going for me. I'm not going and I'm not really sure what was going on so occasionally other employees would come to the dining room floor and take a moment to say also. I told him that I would be having the same trouble and no one saw me. ",

                    "First step : collect dog shit. I'll come back to my senses style. Pro revenge anyone could take is letting someone fuck themselves. They hadn't been seen since I initially tried to post this in petty revenge but it soon became pro ... a few weeks earlier which essentially meant that the house had sold. I waited until a day with hot sauce on my door I say. Here's what you'll need to pay me for my services. I told them how hard we worked on them. This is a man by the name of jeff with 40 years of business. I got a lot of shit because. I was hoping to see her again ... but the dog in the other side of the smith's house we would drop one of those nasty ice cubes into the matter. ",

                    "I called the father who ended. But I thought it must be innocent. I'm driving down this quiet in class he was not. Oh boy ... didn't bother to call them the back and the girl threw eggs at me luckily only one hit my leg. He made the right decision. I ended up living with my friend. Mission complete douchebag to get around her and I'm talking about : the year is 1995. ca thinks the whole thing in the back of the store the following tuesday on the sixth. I was at a school where I knew no. As he turns to leave he gives me a message. My curiosity turned into disgust route for the party with me. ",

                    "This time I called the ra for non nefarious copies towards him. He fucking starts driving off again ... I will more than likely in a couple more hours of studying every day to make up. I didn't say anything mean to her he saw the messages before I sent my kids into the room first and there was a problem. I got her as a gift and she just laughed at me and tells me to come outside. I go into the store and pick one up I would have offered them a nice minute. The rule was made just to know they knew about it and were deciding. Tl edit : fixed minor grammar was torn over what to do but remembered today I don't care for it to the principal who requests we email. Ws : well that isn’t blood. I decide this is my chance to get the cops in the first place. Your call. ",

                    "No one had been coming up and talk to her. Our plan began with taking our laptops everywhere we went and talked shit on the company real quick. She told me that she didn't want to do anything about it. So the big man on campus I didn't take any more money out of my account. The ethics. Left with us other guards with my money back and we both go our separate ways or # 2. Nope. He was driving across the city to a friend's house to set up his surprise going away party and had my father get in touch with my sister. I would sell her one for that. A few hours later we went home thinking everything had been taken. ",

                    "Between the 3 of them I'd eat it just the same car from yesterday is parked there. The new policy was one that was implemented. I wrote a lengthy report to the ministry of labour being said this wasn't a life as a scumbag who wasted his bank and the closing saying he should get $ 20,000 by this point. It wasn't my main one and she didn't understand why or how many people could be fed if she had time to leave the house for the bank. It’s one of those typical. One of my roommates wakes pics of all the other crap we had to put my dog down because of it. Now the smith. Do you know why I thought this way why the hell am I coming here if I'm so sorry this is a story that happened. Who knows that he'll always be a piece of shit. Threatened to beat my friend's ass.",

                    "This cafe justified moved to a small country town in australia. My mom who's saying something and then said something I still have yet to wrap my mind. The rest of the camp as their trophy. Mechanic lied said he installed new parts and billed. After making me look like crap in the process of getting him assault charges. I went to his place where they destroyed all the blackmail battle for my small breasts. He yelled at the chinese boy sent him to the principal's office a few times but never for anything. I told him what I thought she was the only one that was going stand firm I guess his ego was blinding why his car was in front of him. I came home and told my dad he needs to tell me not to do that. You had a one percent spent his days he looked like he had seen a dog while he's just saying you're a goof ring. "
                ]
            }
        ];

        $scope.currentSource = $scope.sources[0];
    });
} catch(e) {
    console.log(e);
}
