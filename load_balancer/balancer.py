# load_balancer/balancer.py

import random
import time
from threading import Thread, Lock

class LoadBalancer:
    def __init__(self, configurations):
        self.configurations = configurations
        self.instances = self.configurations['instances']
        self.instance_health = {instance['id']: True for instance in self.instances}  # monitoring health status of instances
        self.load = {instance['id']: 0 for instance in self.instances}  # monitoring current load on each instance
        self.lock = Lock()
        
    def distribute_requests(self, request):
        """
        Distribute incoming requests to the appropriate service instance.

        Arguments:
        request -- A dictionary containing request data.
        
        Returns:
        instance_id -- The ID of the instance that receives the request.
        """
        with self.lock:
            healthy_instances = [instance for instance in self.instances if self.instance_health[instance['id']]]
            if not healthy_instances:
                raise Exception("No healthy instances available.")

            selected_instance = min(healthy_instances, key=lambda x: self.load[x['id']])
            self.load[selected_instance['id']] += 1
            print(f"Request {request} distributed to instance {selected_instance['id']}")
            return selected_instance['id']

    def monitor_instances(self):
        """
        Monitor the health and load of each service instance.
        Ensure that requests are only sent to healthy instances and balance adjustments are made in real time.
        """
        def _monitor():
            while True:
                with self.lock:
                    for instance in self.instances:
                        instance_id = instance['id']
                        health_status = self.check_instance_health(instance)
                        self.instance_health[instance_id] = health_status
                        if not health_status:
                            print(f"Instance {instance_id} is down.")
                        else:
                            print(f"Instance {instance_id} is healthy.")
                time.sleep(5)

        monitor_thread = Thread(target=_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()

    def check_instance_health(self, instance):
        """
        Simulate the health check of a service instance.

        Arguments:
        instance -- A dictionary containing instance data.
        
        Returns:
        bool -- Health status of the instance (True for healthy, False for down).
        """
        # Placeholder for real health check logic
        return random.choice([True, True, True, False])

    def scale_instances(self):
        """
        Trigger the scaling up or down of instances based on current load demands.
        """
        def _scale():
            while True:
                with self.lock:
                    avg_load = sum(self.load.values()) / len(self.instances)
                    if avg_load > self.configurations['max_load_threshold']:
                        self.add_instance()
                    elif avg_load < self.configurations['min_load_threshold'] and len(self.instances) > self.configurations['min_instances']:
                        self.remove_instance()
                time.sleep(10)

        scale_thread = Thread(target=_scale)
        scale_thread.daemon = True
        scale_thread.start()

    def add_instance(self):
        """
        Add a new instance to handle load.
        """
        new_instance_id = f"instance_{len(self.instances) + 1}"
        new_instance = {'id': new_instance_id, 'url': f"http://{new_instance_id}.example.com"}
        self.instances.append(new_instance)
        self.instance_health[new_instance_id] = True
        self.load[new_instance_id] = 0
        print(f"New instance {new_instance_id} added.")

    def remove_instance(self):
        """
        Remove an instance to balance load.
        """
        for instance in self.instances:
            instance_id = instance['id']
            if self.load[instance_id] == 0:
                self.instances = [inst for inst in self.instances if inst['id'] != instance_id]
                del self.instance_health[instance_id]
                del self.load[instance_id]
                print(f"Instance {instance_id} removed.")
                break
