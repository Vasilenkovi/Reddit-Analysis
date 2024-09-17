from StatApp.views import cloud
from django.test import SimpleTestCase
from wordcloud import WordCloud, STOPWORDS
class cloud_test(SimpleTestCase):
    def setUp(self):
        self.samples = [ """How to explain ZeroMQ? Some of us start by saying all the wonderful things it does. It’s sockets on steroids. It’s like mailboxes with routing. It’s fast! Others try to share their moment of enlightenment, that zap-pow-kaboom satori paradigm-shift moment when it all became obvious. Things just become simpler. Complexity goes away. It opens the mind. Others try to explain by comparison. It’s smaller, simpler, but still looks familiar. Personally, I like to remember why we made ZeroMQ at all, because that’s most likely where you, the reader, still are today.

Programming is science dressed up as art because most of us don’t understand the physics of software and it’s rarely, if ever, taught. The physics of software is not algorithms, data structures, languages and abstractions. These are just tools we make, use, throw away. The real physics of software is the physics of people–specifically, our limitations when it comes to complexity, and our desire to work together to solve large problems in pieces. This is the science of programming: make building blocks that people can understand and use easily, and people will work together to solve the very largest problems.

We live in a connected world, and modern software has to navigate this world. So the building blocks for tomorrow’s very largest solutions are connected and massively parallel. It’s not enough for code to be “strong and silent” any more. Code has to talk to code. Code has to be chatty, sociable, well-connected. Code has to run like the human brain, trillions of individual neurons firing off messages to each other, a massively parallel network with no central control, no single point of failure, yet able to solve immensely difficult problems. And it’s no accident that the future of code looks like the human brain, because the endpoints of every network are, at some level, human brains.

If you’ve done any work with threads, protocols, or networks, you’ll realize this is pretty much impossible. It’s a dream. Even connecting a few programs across a few sockets is plain nasty when you start to handle real life situations. Trillions? The cost would be unimaginable. Connecting computers is so difficult that software and services to do this is a multi-billion dollar business.

So we live in a world where the wiring is years ahead of our ability to use it. We had a software crisis in the 1980s, when leading software engineers like Fred Brooks believed there was no “Silver Bullet” to “promise even one order of magnitude of improvement in productivity, reliability, or simplicity”.

Brooks missed free and open source software, which solved that crisis, enabling us to share knowledge efficiently. Today we face another software crisis, but it’s one we don’t talk about much. Only the largest, richest firms can afford to create connected applications. There is a cloud, but it’s proprietary. Our data and our knowledge is disappearing from our personal computers into clouds that we cannot access and with which we cannot compete. Who owns our social networks? It is like the mainframe-PC revolution in reverse.

We can leave the political philosophy for another book. The point is that while the Internet offers the potential of massively connected code, the reality is that this is out of reach for most of us, and so large interesting problems (in health, education, economics, transport, and so on) remain unsolved because there is no way to connect the code, and thus no way to connect the brains that could work together to solve these problems.

There have been many attempts to solve the challenge of connected code. There are thousands of IETF specifications, each solving part of the puzzle. For application developers, HTTP is perhaps the one solution to have been simple enough to work, but it arguably makes the problem worse by encouraging developers and architects to think in terms of big servers and thin, stupid clients.

So today people are still connecting applications using raw UDP and TCP, proprietary protocols, HTTP, and Websockets. It remains painful, slow, hard to scale, and essentially centralized. Distributed P2P architectures are mostly for play, not work. How many applications use Skype or Bittorrent to exchange data?

Which brings us back to the science of programming. To fix the world, we needed to do two things. One, to solve the general problem of “how to connect any code to any code, anywhere”. Two, to wrap that up in the simplest possible building blocks that people could understand and use easily.

It sounds ridiculously simple. And maybe it is. That’s kind of the whole point.""",
                         """“I am team leader in the company ActForex, which develops software for financial markets. Due to the nature of our domain, we need to process large volumes of prices quickly. In addition, it’s extremely critical to minimize latency in processing orders and prices. Achieving a high throughput is not enough. Everything must be handled in a soft real time with a predictable ultra low latency per price. The system consists of multiple components exchanging messages. Each price can take a lot of processing stages, each of which increases total latency. As a consequence, low and predictable latency of messaging between components becomes a key factor of our architecture.

                         “We investigated different solutions to find something suitable for our needs. We tried different message brokers (RabbitMQ, ActiveMQ Apollo, Kafka), but failed to reach a low and predictable latency with any of them. In the end, we chose ZeroMQ used in conjunction with ZooKeeper for service discovery. Complex coordination with ZeroMQ requires a relatively large effort and a good understanding, as a result of the natural complexity of multithreading. We found that an external agent like ZooKeeper is better choice for service discovery and coordination while ZeroMQ can be used primarily for simple messaging. ZeroMQ fit perfectly into our architecture. It allowed us to achieve the desired latency using minimal efforts. It saved us from a bottleneck in the processing of messages and made processing time very stable and predictable.

                         “I can decidedly recommend ZeroMQ for solutions where low latency is important.
                         When I set out to write a ZeroMQ book, we were still debating the pros and cons of forks and pull requests in the ZeroMQ community. Today, for what it’s worth, this argument seems settled: the “liberal” policy that we adopted for libzmq in early 2012 broke our dependency on a single prime author, and opened the floor to dozens of new contributors. More profoundly, it allowed us to move to a gently organic evolutionary model that was very different from the older forced-march model.

                         The reason I was confident this would work was that our work on the Guide had, for a year or more, shown the way. True, the text is my own work, which is perhaps as it should be. Writing is not programming. When we write, we tell a story and one doesn’t want different voices telling one tale; it feels strange.

                         For me the real long-term value of the book is the repository of examples: about 65,000 lines of code in 24 different languages. It’s partly about making ZeroMQ accessible to more people. People already refer to the Python and PHP example repositories–two of the most complete–when they want to tell others how to learn ZeroMQ. But it’s also about learning programming languages.

                         Here’s a loop of code in Tcl:"""        ]
        self.results = [

        ]

        with open("./StatApp/test1", mode='r') as file:  # b is important -> binary
            self.results.append(file.read())
        with open("./StatApp/test2", mode='r') as file:  # b is important -> binary
            self.results.append(file.read())
        self.stopw = STOPWORDS
    def test_empty_data(self):
        with self.assertRaises(Exception):
            cloud(self.stopw, "")
        with self.assertRaises(Exception):
            cloud([], "")
        for s in range(len(self.samples)):
            with self.assertRaises(Exception):
                cloud([], self.samples[s])
    def test_correct_data(self):
        for s in range(len(self.samples)):
            self.assertTrue(cloud(self.stopw, self.samples[s]))
