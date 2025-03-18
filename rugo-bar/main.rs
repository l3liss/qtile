use x11rb::connection::Connection;
use x11rb::protocol::xproto::*;
use tray_item::TrayItem;

fn main() {
    let (conn, screen_num) = x11rb::connect(None).unwrap();
    let screen = &conn.setup().roots[screen_num];

    // Create window for the bar
    let win = conn.generate_id().unwrap();
    conn.send_request(&CreateWindow {
        depth: 0,
        wid: win,
        parent: screen.root,
        x: 0,
        y: 0,
        width: screen.width_in_pixels,
        height: 30, // 30px high
        border_width: 0,
        class: WindowClass::INPUT_OUTPUT,
        visual: screen.root_visual,
        value_list: &CreateWindowAux::default(),
    });

    // Set _NET_WM_WINDOW_TYPE to DOCK
    let dock_atom = conn.intern_atom(false, b"_NET_WM_WINDOW_TYPE_DOCK").unwrap();
    conn.change_property8(PropMode::REPLACE, win, dock_atom.reply().unwrap().atom, AtomEnum::CARDINAL, &[1]);

    // Set reserved space (_NET_WM_STRUT_PARTIAL)
    let strut: [u32; 12] = [0, 0, 0, 30, 0, 0, 0, 0, 0, screen.width_in_pixels, 0, 0];
    conn.change_property32(PropMode::REPLACE, win, dock_atom.reply().unwrap().atom, AtomEnum::CARDINAL, &strut);

    // Create System Tray
    let mut tray = TrayItem::new("Rust Bar", "icon-name").unwrap();
    tray.add_label("System Tray").unwrap();

    // Map window and run
    conn.map_window(win);
    conn.flush();
    
    loop {} // Keep the bar running
}
