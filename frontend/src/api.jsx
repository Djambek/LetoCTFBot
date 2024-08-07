const API_URL = "https://ctf.djambek.com/api"
export function init_api(id) {
	const request = new XMLHttpRequest();
	request.open("POST", API_URL + "/login", false);
	request.setRequestHeader('Content-Type', 'application/json');
	request.send(JSON.stringify({id : id}));
}

export function get_top() {
	const request = new XMLHttpRequest();
	request.open("GET", API_URL + "/top", false);
	request.setRequestHeader('Content-Type', 'application/json');
	request.send(null);
	let r = JSON.parse(request.responseText);
	let res = r.map((e) => ({
		points: e.hp,
		name: e.name,
		avatar: e.avatar
	}));
	return Array(...res);
}

export function get_profile() {
	const request = new XMLHttpRequest();
	request.open("GET", API_URL + "/profile", false);
	request.send(null);
	let r = JSON.parse(request.responseText);

	return {
		username: r.name,
		avatar: r.avatar,
		health: r.hp,
		damage: r.attack,
	};
}

export function use_item(id) {
	const request = new XMLHttpRequest();
	request.open("GET", API_URL + "/use/" + id, false);
	request.send(null);
	console.log("Use item", id);
}

export function get_items() {
	const request = new XMLHttpRequest();
	request.open("GET", API_URL + "/inventory", false);
	request.send(null);	
	let r = JSON.parse(request.responseText);
	let res = r.map((e) => ({ id: e.id, name: e.name, icon: e.icon, effect: e.hp }))
	console.log(res);
	return Array(...res);
}

export function get_events() {
	return Array(
		{is_registered: false, id: 1, name: "event 1", description: "skuf", time: "08:26:46.182000", place: "zhopa", team_size: 1, duration: 10, no_damage: true},
		{is_registered: true, id: 2, name: "event 2", description: "skuf", time: "08:26:46.182000", place: "pizda", team_size: 2, duration: 500, no_damage: false},
		{is_registered: true, id: 3, name: "event 3", description: "meow", time: "01:00:01.969696", place: ":3", team_size: 7, duration: 30, no_damage: false},
	);
}

