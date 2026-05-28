import random
from models.link import Link

class ChaosMonkey:
    def __init__(self, topo, sim, original_links):
        self.topo = topo
        self.sim = sim
        self.original_links = original_links
        self.broken_links = []
        self.is_active = False

    def trigger_random_event(self):
        if not self.is_active: return

        # Tung xúc xắc
        action = random.choice(["BREAK", "BREAK", "RESTORE"])

        if action == "BREAK" and len(self.topo.links) > 10: 
            link_to_break = random.choice(self.topo.links)
            src, dst = link_to_break.source_id, link_to_break.dest_id
            
            # --- THÔNG BÁO LỚN RA TERMINAL ---
            print(f"\n{'='*50}")
            print(f"🚨 [SỰ KIỆN MẠNG] ĐỨT CÁP: Tuyến {src} <---> {dst} đã mất kết nối!")
            print(f"{'='*50}\n")
            
            self.topo.remove_link(src, dst)
            self.topo.remove_link(dst, src)
            self.broken_links.append((src, dst))

        elif action == "RESTORE" and self.broken_links:
            src, dst = self.broken_links.pop(0)
            
            # --- THÔNG BÁO LỚN RA TERMINAL ---
            print(f"\n{'='*50}")
            print(f"🛠️ [SỰ KIỆN MẠNG] HỒI PHỤC: Tuyến {src} <---> {dst} đã được nối lại!")
            print(f"{'='*50}\n")
            
            bw = 100.0; dly = 1.0
            for l in self.original_links:
                if l.source_id == src and l.dest_id == dst:
                    bw = l.bandwidth; dly = l.delay; break
                    
            self.topo.add_link(Link(src, dst, bw, delay=dly))
            self.topo.add_link(Link(dst, src, bw, delay=dly))
            
            self.topo.flood_lsa(src, self.topo.routers[src].generate_lsa())
            self.topo.flood_lsa(dst, self.topo.routers[dst].generate_lsa())

        next_delay = random.uniform(30.0, 100.0)
        self.sim.schedule(next_delay, "CHAOS_MONKEY", self.trigger_random_event)
