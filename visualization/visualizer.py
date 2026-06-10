import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from utils.config import Config

class OSPFVisualizer:
    def __init__(self, topology, simulator, pos, chaos_monkey):
        self.topology = topology
        self.simulator = simulator
        self.pos = pos
        self.chaos_monkey = chaos_monkey
        
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.25) 
        self.is_paused = False
        
        # --- BẢNG ĐIỀU KHIỂN ---
        ax_pause = self.fig.add_axes([0.15, 0.05, 0.15, 0.075])
        self.btn_pause = Button(ax_pause, 'Tạm dừng Mô phỏng')
        self.btn_pause.on_clicked(self.toggle_pause)
        
        ax_break = self.fig.add_axes([0.35, 0.05, 0.25, 0.075])
        self.btn_break = Button(ax_break, 'Bật Sự Cố Ngẫu Nhiên', color='lightcoral')
        self.btn_break.on_clicked(self.toggle_chaos)

        ax_table = self.fig.add_axes([0.65, 0.05, 0.2, 0.075])
        self.btn_table = Button(ax_table, 'In Bảng định tuyến R1', color='lightgreen')
        self.btn_table.on_clicked(self.print_table)

    def toggle_pause(self, event):
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            print("\n[GUI] ĐÃ TẠM DỪNG mô phỏng.")
            self.btn_pause.label.set_text('Tiếp tục Mô phỏng')
            self.btn_pause.color = 'lightblue'  
        else:
            print("\n[GUI] ĐANG CHẠY mô phỏng.")
            self.btn_pause.label.set_text('Tạm dừng Mô phỏng')
            self.btn_pause.color = '0.85'  

        self.fig.canvas.draw_idle()

    def toggle_chaos(self, event):
        self.chaos_monkey.is_active = not self.chaos_monkey.is_active
        if self.chaos_monkey.is_active:
            print("\n[GUI] Kích hoạt Chaos Monkey: Các sự cố đứt mạng và khôi phục sẽ xảy ra ngẫu nhiên!")
            self.chaos_monkey.trigger_random_event() 
            self.btn_break.color = 'orange'
            self.btn_break.label.set_text('Tắt Sự Cố Ngẫu Nhiên')
        else:
            print("\n[GUI] Tắt Chaos Monkey.")
            self.btn_break.color = 'lightcoral'
            self.btn_break.label.set_text('Bật Sự Cố Ngẫu Nhiên')

    def print_table(self, event):
        if "R1" in self.topology.routers:
            print(f"\n[GUI] BẢNG ĐỊNH TUYẾN HIỆN TẠI CỦA R1 (Tại ms {self.simulator.current_time:.1f}):")
            self.topology.routers["R1"].routing_table.display()

    def update(self, frame):
        if not self.is_paused:
            if self.simulator.event_queue:
                self.simulator.step()
                
        self.ax.clear()
        self.ax.set_title(f"OSPF {len(self.topology.routers)}-Node Simulator | Thời gian: {self.simulator.current_time:.1f} ms", fontsize=15, fontweight='bold')
        
        G = nx.Graph()
        for r_id in self.topology.routers:
            G.add_node(r_id)
        for link in self.topology.links:
            if not G.has_edge(link.source_id, link.dest_id):
                G.add_edge(link.source_id, link.dest_id, cost=link.cost)
            
        if len(G.nodes) > 0:
            active_edges = set()
            if "R1" in self.topology.routers:
                rt = self.topology.routers["R1"].routing_table
                for dest, entry in rt.entries.items():
                    path = entry.path
                    for i in range(len(path) - 1):
                        active_edges.add((path[i], path[i+1]))
                        active_edges.add((path[i+1], path[i]))

            edge_colors = []
            edge_widths = []
            for u, v in G.edges():
                if (u, v) in active_edges:
                    edge_colors.append(Config.COLOR_ACTIVE_PATH)
                    edge_widths.append(Config.ACTIVE_EDGE_WIDTH)
                else:
                    edge_colors.append(Config.COLOR_IDLE_PATH)
                    edge_widths.append(Config.IDLE_EDGE_WIDTH)

            node_colors = [Config.COLOR_ROOT_NODE if node == 'R1' else Config.COLOR_NORMAL_NODE for node in G.nodes()]
            
            nx.draw_networkx_nodes(G, self.pos, ax=self.ax, node_color=node_colors, node_size=Config.NODE_SIZE, edgecolors='black')
            nx.draw_networkx_labels(G, self.pos, ax=self.ax, font_size=Config.FONT_SIZE, font_weight='bold')
            nx.draw_networkx_edges(G, self.pos, ax=self.ax, width=edge_widths, edge_color=edge_colors)
            
            edge_labels = nx.get_edge_attributes(G, 'cost')
            nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, ax=self.ax, font_color='black')
        
        self.ax.axis('off')

    def start(self):
        self.anim = FuncAnimation(self.fig, self.update, interval=Config.ANIMATION_INTERVAL, cache_frame_data=False)
        plt.show()
