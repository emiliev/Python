import uuid
import math
import datetime

class User():

    def __init__(self, name):
        self.full_name = name
        self.uuid = uuid.uuid4()
        self.posts = []
        self.followers = set()

    def add_post(self, post_content):
        new_post = Post(self.uuid,post_content)
        self.posts.append(new_post)
        if len(self.posts) > 50:
            self.posts[1] = self.posts[1:]


    def get_post(self):
        return (post for post in self.posts)

    def add_follower(self, uuid):
        self.followers.add(uuid)

    def remove_follower(self, uuid):
        self.followers.discard(uuid)

    def show_followers(self):
        return self.followers

    def search_follower(self,uuid):
        if uuid in self.followers:
            return True
        return False


class Post():
    
    def __init__(self, author, content):
        self.author = author
        self.published_at = datetime.datetime.now()
        self.content = content


class SocialGraph():
    
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.uuid in self.users:
            raise UserAlreadyExistsError
        self.users[user.uuid] = user

    def get_user(self, user_uuid):
        if user_uuid not in self.users:
            raise UserDoesNotExistError
        return self.users[user_uuid]
    
    #da se triqt i sledvanite
    def delete_user(self, user_uuid):
        if user_uuid not in self.users:
            raise UserDoesNotExistError
        del self.users[user_uuid]


#exceptionii navsqkude -UDNErr
    def follow(self, follower, followee):
        #userfollower error
        if follower == followee:
            raise UserFollowError
        self.users[followee].add_follower(follower)
    
    def unfollow(self, follower, followee):
        self.users[followee].remove_follower(follower)

    def is_following(self, follower, followee):
        return self.users[followee].search_follower(follower)

    def followers(self, user_uuid):
        return self.users[user_uuid].show_followers()

    def following(self, user_uuid):
        return {customer for customer in self.users 
                if self.is_following(user_uuid, customer)}

    def friends(self, user_uuid):
        return {customer for customer in self.users
                if self.is_following(user_uuid, customer) and
                self.is_following(customer, user_uuid)}
#aka DFS
    def max_distance(self, user_uuid):
        visited = set()
        queue = ['#',user_uuid]
        distance = 0
        while queue:
            vertex = queue.pop(0)
            print(vertex)
            if vertex not in visited and vertex != '#':
                visited.add(vertex)
                queue.extend(self.following(vertex) - visited )
            elif vertex is '#' and len(queue) > 0:
                queue.append('#')
                print(distance)
                distance +=1

        return distance - 1

    def min_distance(self, from_user_uuid, to_user_uuid):
        queue = []
        queue.append([from_user_uuid])
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == to_user_uuid:
                return len(path) - 1
            for adjacent in self.following(node):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
        raise UsersNotConnectedError

    def nth_layer_followings(self, user_uuid, n):
        visited = set()
        queue = [user_uuid]
        nth_level_followings = []
        for level in range(n):
            level_nodes = len(queue)
            for index in range(level_nodes):
                node = queue.pop(0)
                if node not in visited and level < n - 1:
                    visited.add(node)
                    queue.extend(self.following(node) - visited)
                elif node not in visited and level == n - 1:
                    nth_level_followings.extend(self.following(node) - visited)
        return nth_level_followings


    def generate_feed(self, user_uuid, offset=0, limit=10):
        feed = [post for user in self.following(user_uuid)
                for post in self.get_user(user).get_post()]
        feed.sort(key=lambda p: p.published_at, reverse=True)
        return feed[offset: offset + limit: 1]


class UserDoesNotExistError(Exception):
    pass    


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


class UserFollowError(Exception):
    pass


graph = SocialGraph()
eric = User("Eric")
gram = User("Graham")
john = User("John")
michael = User("Meter")
terry = User("Tosho")

graph.add_user(eric)
graph.add_user(gram)
graph.add_user(john)
graph.add_user(michael)
graph.add_user(terry)
graph.follow(terry.uuid,eric.uuid)
graph.follow(terry.uuid, gram.uuid)
graph.follow(eric.uuid,michael.uuid)
graph.follow(eric.uuid, john.uuid)
graph.follow(john.uuid,gram.uuid)

print(graph.max_distance(terry.uuid))
# print(graph.max_distance(eric.uuid))
# print(graph.min_distance(eric.uuid,eric.uuid))
# print(graph.min_distance(terry.uuid,gram.uuid))
# print(graph.nth_layer_followings(terry.uuid, 1))


for index in range(51):
    eric.add_post("spam")

for post in eric.get_post():
    print(post.content)


