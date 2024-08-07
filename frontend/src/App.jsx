import React from 'react';

import '@telegram-apps/telegram-ui/dist/styles.css';
import styles from './App.module.css';
import { 
	AppRoot, 
	Avatar, 
	Cell, 
	Info, 
	TabsList, 
	Chip, 
	List, 
	Text
} from '@telegram-apps/telegram-ui';
import Inventory from './Inventory.jsx';
import Events from './Events.jsx';
import { init_api, get_top, get_profile } from './api.jsx';

const UserInfo = (props) => { 
	const empty_heart = <i className={ "icon-heart-empty " + styles.heart }> </i>
	const filled_heart = <i className={ "icon-heart " + styles.heart }> </i>

	let hp = Array(
		<span>{ props.health } </span>,
		<i className={ "icon-heart " + styles.heart }> </i>
	);
	let atk = Array(
		<span className={ styles.highlight }>{ props.damage }</span>,
		<span className={ "material-symbols-outlined " + styles.sword + ' ' + styles.highlight }> swords </span>
	);


	return (
		<Cell
			className={ styles.userinfo }
			before={ <Avatar size={96} src={ props.avatar } />}
			subtitle={ props.team }
			hovered={ true }
			after={ (
				<div>
					<Info className={ styles.healthbar }> { hp } </Info>
					<Info className={ styles.attackbar }> { atk } </Info>
				</div>
			)}
		>
		{ props.username }	
		</Cell>
	);
}

const TabsItem = TabsList.Item;
const TopTableItem = (props) => {
	let highlight = '';
	if(props.name === props.username)
		highlight = ' ' + styles.highlight;
	return (<tr>
		<td className={styles.teamhash + highlight}>#{props.idx}</td>
		<td className={styles.teamavatar}><Avatar size={42} src={props.avatar}></Avatar></td>
		<td className={styles.teamname + highlight}>{props.name}</td>
		<td className={styles.teampoints + highlight}>{props.points}</td>
	</tr>);
}

class MainUI extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
		
		// let tg = window.Telegram.WebApp;
		// let user = tg.initDataUnsafe.user;
		
		init_api(/* user.id */ 511612441);
		let r = get_profile();

		this.state = {
			username: r.username,
			avatar: r.avatar,
			health: r.health,
			damage: r.damage,
			tab: { inventory: true },
			team: r.username,
			avatar: r.avatar,
			page: this.inventory(),
		};
	}
	
	inventory_tab() {
		this.setState({ 
			tab: { inventory: true },
			page: this.inventory(),
		});
	}
	events_tab() {
		this.setState({ 
			tab: { events: true },
			page: this.events(),
		});
	}
	top_tab() {
		this.setState({ 
			tab: { top: true },
			page: this.top(this.state.username),
		});
	}

	inventory () {
		return (
			<Inventory app={this} {...this.state} />
		);
	}

	events() {
		return (
			<Events app={this} {...this.state} />
		)
	}
	
	top(username) {

		let table = get_top().map((e, i) =>
			<TopTableItem username={ username } {...e} idx={i+1} key={i}/>
		);
		return (
			<table className={styles.toptable}> 
				<tbody>
					{table} 
				</tbody>
			</table>
		);
	}

	render() {
		return (
				<div>
					<UserInfo
						{...this.state}
						key="user_info"
					/>
					<TabsList 
						key="navbar"
						style={{
							background: 'var(--dark)'
						}}
					>
						<TabsItem
							selected={this.state.tab.top}
							onClick={() => this.top_tab()}
						>
							Top
						</TabsItem>
						<TabsItem 
							selected={this.state.tab.inventory}
							onClick={() => this.inventory_tab()}
						> 
							Inventory
						</TabsItem>
						<TabsItem 
							selected={this.state.tab.events}
							onClick={() => this.events_tab()}
						>
							Events
						</TabsItem>
					</TabsList>
					{this.state.page}
				</div>
		);
	}
}

const App = () => (
	<AppRoot>
		<MainUI className=""/>
	</AppRoot>
);

export default App;



